import pygame


DEFAULT_COLORKEY = (0, 255, 0)


class AssetPool:
    sprites = {}

    @staticmethod
    def load_all_sprites():
        # goes through every file in specific folder (e.g. images/sprites)
        # and loads them
        pass

    @staticmethod
    def get_sprite(resource_name, has_alpha=False):
        # TODO: implement absolute pathing
        if resource_name in AssetPool.sprites:
            return AssetPool.sprites[resource_name]
        else:
            # these checks don't apply for resource loading...
            if has_alpha:
                image = pygame.image.load(resource_name).convert_alpha()
            else:
                image = pygame.image.load(resource_name).convert()
            AssetPool.sprites[resource_name] = image
            return image

    @staticmethod
    def set_colorkey(resource_name, colorkey=DEFAULT_COLORKEY):
        if resource_name in AssetPool.sprites:
            AssetPool.sprites[resource_name] = AssetPool.sprites[resource_name].set_colorkey(colorkey)
        else:
            print("[SetColorKey] Resource not found")

