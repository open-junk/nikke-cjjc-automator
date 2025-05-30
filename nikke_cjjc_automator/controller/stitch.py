class ImageStitcher:
    """圖片拼接工具，抽象化水平與垂直拼接"""
    def __init__(self, hotkey_mgr):
        self.hotkey_mgr = hotkey_mgr

    def stitch(self, image_paths, output_path, direction="vertical", spacing=0, background_color=(0,0,0)):
        self.hotkey_mgr.check()
        from PIL import Image
        from pathlib import Path
        import logging
        images = [Image.open(p) for p in image_paths if Path(p).exists()]
        if not images:
            logging.error("無有效圖片可拼接")
            return False
        match direction:
            case "vertical":
                max_width = max(img.width for img in images)
                total_height = sum(img.height for img in images) + spacing * (len(images)-1)
                stitched = Image.new('RGB', (max_width, total_height), color=background_color)
                y = 0
                for img in images:
                    stitched.paste(img, (0, y))
                    y += img.height + spacing
                    img.close()
            case "horizontal":
                total_width = sum(img.width for img in images) + spacing * (len(images)-1)
                max_height = max(img.height for img in images)
                stitched = Image.new('RGB', (total_width, max_height), color=background_color)
                x = 0
                for img in images:
                    stitched.paste(img, (x, 0))
                    x += img.width + spacing
                    img.close()
            case _:
                logging.error(f"未知拼接方向: {direction}")
                return False
        stitched.save(output_path)
        return True
