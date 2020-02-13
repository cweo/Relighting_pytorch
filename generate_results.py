from PIL import Image
import glob
import os

def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    ref: https://stackoverflow.com/a/46623632
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

if __name__=='__main__':
    # thumbnail1
    line_1_files = sorted(glob.glob(os.path.join('./results/', 'thumbnail1', 'real', '*.png')))
    line_2_files = sorted(glob.glob(os.path.join('./results/', 'thumbnail1', '4500', '*.png')))
    line_3_files = sorted(glob.glob(os.path.join('./results/', 'thumbnail1', '4500_linear', '*.png')))
    line_4_files = sorted(glob.glob(os.path.join('./results/', 'thumbnail1', '6500', '*.png')))
    line_5_files = sorted(glob.glob(os.path.join('./results/', 'thumbnail1', '6500_linear', '*.png')))    
    # Load images
    load_resize = lambda file_path: Image.open(file_path).resize((256,256), Image.BICUBIC)
    images_1 = list(map(load_resize, line_1_files))
    images_2 = list(map(Image.open, line_2_files))
    images_3 = list(map(Image.open, line_3_files))
    images_4 = list(map(Image.open, line_4_files))
    images_5 = list(map(Image.open, line_5_files))
    # Conc. horizontal
    combo_1 = append_images(images_1, direction='horizontal')
    combo_2 = append_images(images_2, direction='horizontal')
    combo_3 = append_images(images_3, direction='horizontal')
    combo_4 = append_images(images_4, direction='horizontal')
    combo_5 = append_images(images_5, direction='horizontal')
    # Conc. vertical
    combo_final = append_images([combo_1, combo_2, combo_3, combo_4, combo_5], direction='vertical')
    # Save image
    combo_final.save(os.path.join('./results/', 'thumbnail1', 'thumbnail1.png'))
        