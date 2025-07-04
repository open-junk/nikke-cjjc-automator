class ImageStitcher:
    """Image stitching utility, abstracts vertical and horizontal stitching"""
    def __init__(self, hotkey_mgr):
        self.hotkey_mgr = hotkey_mgr

    def stitch(self, image_paths, output_path, direction="vertical", spacing=0, background_color=(0,0,0)):
        self.hotkey_mgr.check()
        from PIL import Image
        from pathlib import Path
        import logging
        # Force check: image_paths must contain valid images, otherwise raise error
        images = [Image.open(p) for p in image_paths]
        # Use the output_path provided by the caller directly, do not move to result_image
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if direction == "vertical":
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images) + spacing * (len(images)-1)
            stitched = Image.new('RGB', (max_width, total_height), color=background_color)
            y = 0
            for img in images:
                stitched.paste(img, (0, y))
                y += img.height + spacing
                img.close()
        elif direction == "horizontal":
            total_width = sum(img.width for img in images) + spacing * (len(images)-1)
            max_height = max(img.height for img in images)
            stitched = Image.new('RGB', (total_width, max_height), color=background_color)
            x = 0
            for img in images:
                stitched.paste(img, (x, 0))
                x += img.width + spacing
                img.close()
        else:
            logging.error(f"Unknown stitching direction: {direction}")
            return False
        stitched.save(output_path)
        return True
