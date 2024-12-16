import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import imageio
from PIL import Image

def generate_grating_pattern_rgba(n_pix=200, freq=16, sig=0.5, r_annulus=0.2, 
                                  phase_shift=4 * np.pi/3, beef_factor=0.6, 
                                  angle=0, pattern_color=(1, 1, 1), 
                                  background_color=(0, 0, 0), border_thickness=0, 
                                  border_color=(1, 1, 1), checker_size=0, 
                                  checker_scale=8, checker_thickness=4,
                                  save_img=False, filename='grating_with_checker.png'):
    # Define a custom RGBA dtype
    rgba_dtype = np.dtype([('r', np.float32), ('g', np.float32), ('b', np.float32), ('a', np.float32)])

    # Create 2D grid
    x = np.linspace(-np.pi, np.pi, n_pix)
    y = np.linspace(-np.pi, np.pi, n_pix)
    X, Y = np.meshgrid(x, y)

    # Rotate the grid by the specified angle
    theta = np.radians(angle)
    X_rot = X * np.cos(theta) + Y * np.sin(theta)
    
    # Create sine wave grating for the rotated grid
    grating = np.sin((freq * X_rot + phase_shift)) + beef_factor

    # Normalize grating between 0 and 1
    grating = np.clip((grating + 1) / 2, 0, 1)

    # Create Gaussian masking envelope
    mask = np.exp(-(X**2 + Y**2) / (2 * sig**2))
    mask = (mask - np.min(mask)) / (np.max(mask) - np.min(mask))

    # Create annulus mask
    annulus_mask = np.float64(X**2 + Y**2 > r_annulus**2)
    annulus_mask = gaussian_filter(annulus_mask, 0.01 * n_pix)  # Smooth edges of annulus
    annulus_mask = (annulus_mask - np.min(annulus_mask)) / (np.max(annulus_mask) - np.min(annulus_mask))
    mask = mask * annulus_mask

    # Apply mask to the grating
    intensity = grating * mask

    # Initialize RGBA image using the custom dtype
    img = np.zeros((n_pix, n_pix), dtype=rgba_dtype)
    img['r'] = pattern_color[0] * intensity
    img['g'] = pattern_color[1] * intensity
    img['b'] = pattern_color[2] * intensity
    img['a'] = mask

    # Add background color
    background = np.zeros((n_pix, n_pix, 4), dtype=np.float32)
    background[:, :, 0] = background_color[0]
    background[:, :, 1] = background_color[1]
    background[:, :, 2] = background_color[2]
    background[:, :, 3] = 1  # Full opacity for background

    # Combine pattern with background
    final_img = background
    alpha = img['a'][..., np.newaxis]
    final_img[:, :, :3] = background[:, :, :3] * (1 - alpha) + np.dstack((img['r'], img['g'], img['b'])) * alpha

    # Add border if specified
    if border_thickness > 0:
        final_img[:border_thickness, :, :3] = border_color
        final_img[-border_thickness:, :, :3] = border_color
        final_img[:, :border_thickness, :3] = border_color
        final_img[:, -border_thickness:, :3] = border_color

    # Add checker frame if specified
    if checker_size > 0:
        checker = np.ones((checker_size, checker_size, 4), dtype=np.uint8) * 255
        checker[:, :, 3] = np.random.choice([0, 0, 255], (checker_size, checker_size))
        checker[checker_thickness:checker_size-checker_thickness, checker_thickness:checker_size-checker_thickness, 3] = 0
        
        # Scale up the checker pattern
        checker = np.repeat(checker, checker_scale, axis=0)
        checker = np.repeat(checker, checker_scale, axis=1)
        
        # Resize or crop checker to match `final_img`
        if checker.shape[0] < n_pix or checker.shape[1] < n_pix:
            pad_x = (n_pix - checker.shape[0]) // 2
            pad_y = (n_pix - checker.shape[1]) // 2
            checker = np.pad(checker, ((pad_x, n_pix - checker.shape[0] - pad_x), 
                                       (pad_y, n_pix - checker.shape[1] - pad_y), 
                                       (0, 0)), mode='constant', constant_values=0)
        else:
            checker = checker[:n_pix, :n_pix, :]

        # Overlay the checker frame on the final image
        checker_alpha = checker[:, :, 3] / 255.0
        final_img[:, :, :3] = final_img[:, :, :3] * (1 - checker_alpha[..., np.newaxis]) + checker[:, :, :3] / 255.0 * checker_alpha[..., np.newaxis]

    # Save the image if required
    if save_img:
        imageio.imsave(filename, (final_img * 255).astype(np.uint8))
        print(f"Image saved as {filename}")

if __name__ == "__main__":
    # Generate grating patterns with borders and checkers
    generate_grating_pattern_rgba(n_pix=500, angle=180, pattern_color=(1, 0, 0), 
                                   background_color=(0, 0, 0), border_thickness=0, 
                                   border_color=(0, 0, 0), checker_size=40, 
                                   checker_scale=8, checker_thickness=4, 
                                   save_img=True, filename="../stimuli/r_v_with_checker.png")

    generate_grating_pattern_rgba(n_pix=500, angle=90, pattern_color=(0, 0, 1), 
                                   background_color=(0, 0, 0), border_thickness=0, 
                                   border_color=(0, 0, 0), checker_size=40, 
                                   checker_scale=8, checker_thickness=4, 
                                   save_img=True, filename="../stimuli/b_h_with_checker.png")

