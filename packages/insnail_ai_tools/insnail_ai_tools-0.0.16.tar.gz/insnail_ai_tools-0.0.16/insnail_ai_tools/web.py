def create_fast_api_app(cors: bool = True, health_check: bool = True, **kwargs):
    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware

    app = FastAPI(**kwargs)
    if cors:
        # 跨域
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if health_check:

        @app.get("/health-check")
        async def health_check_view():
            return {"code": "0000", "msg": "health"}

    return app


def create_flask_app(
    import_name: str, cors: bool = True, health_check: bool = True, **kwargs
):
    from flask import Flask, jsonify
    from flask_cors import CORS

    app = Flask(import_name, **kwargs)
    if cors:
        CORS(app)

    if health_check:

        @app.route("/health-check", methods=["GET"])
        def health_check_view():
            return jsonify({"code": "0000", "msg": "health"})

    return app
