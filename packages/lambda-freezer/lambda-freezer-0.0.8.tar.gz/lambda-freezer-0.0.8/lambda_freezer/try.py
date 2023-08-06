from lambda_freezer import run_after_default_deployment, deploy

if __name__ == "__main__":
    APILIB_REST_API_ID = "hdngkk8dsc"
    APILIB_REGION = "ap-southeast-1"
    APILIB_DOMAIN_NAME = "ea-api-uat.bambu.life"
    APILIB_DEFAULT_ALIAS_NAME = "uat"

    run_after_default_deployment(APILIB_REST_API_ID, APILIB_REGION, APILIB_DEFAULT_ALIAS_NAME, APILIB_DOMAIN_NAME)
    # deploy(APILIB_REST_API_ID, APILIB_REGION, "1.0.1", "some description!", APILIB_DOMAIN_NAME)
