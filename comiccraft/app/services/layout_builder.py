def build_comic_layout(story_panels, image_paths):
    return [{**panel, 'image_path': image_path} for panel, image_path in zip(story_panels, image_paths)]
