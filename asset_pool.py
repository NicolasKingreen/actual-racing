import pygame


class AssetPool:
    sprites = {}

    @staticmethod
    def get_sprite(resource_name):
        # TODO: implement absotule pathing
        if resource_name in AssetPool.sprites:
            return AssetPool.sprites[resource_name]
        else:
            image = pygame.image.load(resource_name)
            AssetPool.sprites[resource_name] = image
            return image

