from app.api.routes.v1.test import router as v1_test_router
from app.api.routes.v1.file_upload_api import router as v1_file_upload_router

main_routers = [
    v1_test_router,
    v1_file_upload_router,
]