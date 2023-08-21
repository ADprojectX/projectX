# videogenerator/routers.py

class MongoDBRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ in ['ProjectAssets', 'Scene']:
            return 'mongoDB'
        return None

    def db_for_write(self, model, **hints):
        if model.__name__ in ['ProjectAssets', 'Scene']:
            return 'mongoDB'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        allowed_models = ['ProjectAssets', 'Scene']
        if obj1.__class__.__name__ in allowed_models or obj2.__class__.__name__ in allowed_models:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'mongoDB':
            allowed_models = ['ProjectAssets', 'Scene']
            return model_name in allowed_models
        return None


# class MongoDBRouter:
#     def db_for_read(self, model, **hints):
#         if model.__name__ == 'Script':
#             return 'mongoDB'
#         return None

#     def db_for_write(self, model, **hints):
#         if model.__name__ == 'Script':
#             return 'mongoDB'
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1.__class__.__name__ == 'Script' or obj2.__class__.__name__ == 'Script':
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if db == 'mongoDB':
#             return model_name == 'Script'
#         return None
