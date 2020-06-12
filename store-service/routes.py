from views import index, get_item, post_item, del_item, patch_item

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/v1/item', get_item)
    app.router.add_post('/v1/item', post_item)
    app.router.add_get('/v1/item/{id}', get_item)
    app.router.add_patch('/v1/item/{id}', patch_item)
    app.router.add_delete('/v1/item/{id}', del_item)

