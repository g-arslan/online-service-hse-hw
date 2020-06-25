from views import index, post_signup, post_signin, post_validate, post_refresh

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/signup', post_signup)
    app.router.add_post('/signin', post_signin)
    app.router.add_post('/validate', post_validate)
    app.router.add_post('/refresh', post_refresh)
