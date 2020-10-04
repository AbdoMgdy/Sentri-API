def register_routes(app, api):

    from app.item import register_routes as  attach_item
    from app.category import register_routes as attach_category
    from app.order import register_routes as attach_order
    from app.catalog import register_routes as attach_catalog
    from app.customer import register_routes as attach_customer
    from app.vendor import register_routes as attach_vendor
    from app.webhook import routes as webhook_routes
    from app.webview import routes as webview_routes

    # Add routes
    attach_item(app, api)
    attach_category(app, api)
    attach_catalog(app, api)
    attach_order(app, api)
    attach_customer(app, api)
    attach_vendor(app, api)
    app.register_blueprint(webhook_routes.webhook_bp)
    app.register_blueprint(webview_routes.webview_bp)
