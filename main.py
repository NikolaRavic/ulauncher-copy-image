import os
import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction


class CopyImageToClipboardAction(ExtensionCustomAction):
    def __init__(self, image_path):
        self._image_path = image_path

    def run(self):
        subprocess.call(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', self._image_path])
        return None


class CopyImageToClipboardListener(EventListener):
    def on_event(self, event, extension):
        if isinstance(event, ItemEnterEvent):
            item = event.get_data()
            action = item.get_action()

            if isinstance(action, CopyImageToClipboardAction):
                action.run()


class LocalImagesSearchExtension(Extension):
    def __init__(self):
        super(LocalImagesSearchExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, CopyImageToClipboardListener())

    def search(self, query):
        image_dir = os.path.expanduser("~/Pictures")
        images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")]

        results = []
        for image in images:
            if query in image:
                results.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=image,
                        description='Copy image to clipboard',
                        on_enter=CopyImageToClipboardAction(image)
                    )
                )

        return results


if __name__ == '__main__':
    LocalImagesSearchExtension().run()
