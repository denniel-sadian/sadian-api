from django.core.files.storage import FileSystemStorage


class MediaFileStorage(FileSystemStorage):
    location = 'media'
    
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name