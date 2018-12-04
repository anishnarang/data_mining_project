from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from flow_handler import FlowHandler

class GetSimilarUsers(Resource):
    def get(self, user_name):
        try:
            result = {}

            if flow_handler_object.exists_user(user_name=user_name):
                result["input_user_login"] = True
                result["similar_users"] = flow_handler_object.get_similar_users(user_name=user_name)
                result["status"] = "SUCCESS"
            else:
                result["input_user_login"] = False
                result["similar_users"] = []
                result["status"] = "FAILED"
                result["Error"] = "Given user not found in out database!"
            return result
        except Exception as e:
            print("Exception:" + str(e))
            return {
                "status" : "FAILED",
                "Error": str(e)
            }

class GetFoodRecommendation(Resource):
    def get(self, user_name_1, user_name_2):
        try:
            result = {}
            print(user_name_1,user_name_2)
            result["recommended_food"] = flow_handler_object.get_food_recommendation(user_name_1, user_name_2)
            result["status"] = "SUCCESS"

            return result
        except Exception as e:
            print("Exception:" + str(e))
            result["status"] = "FAILED"
            result["Error"] = str(e)

            return result

class GetHotelRecommendation(Resource):
    def get(self, food_name):
        try:
            result = {}

            result["recommended_hotels"] = flow_handler_object.get_hotel_recommendation(food_name)
            print(result["recommended_hotels"])
            result["status"] = "SUCCESS"

            return result
        except Exception as e:
            print("Exception:"+str(e))
            result["status"] = "FAILED"
            result["Error"] = str(e)

            return result

if __name__=="__main__":
    try:
        app = Flask(__name__)
        CORS(app)
        api = Api(app)

        # Initialize Flow-handler

        flow_handler_object = FlowHandler()

        # Add resources
        api.add_resource(GetSimilarUsers, "/similar_users/<user_name>")
        api.add_resource(GetFoodRecommendation, "/food_recommendation/<user_name_1>/<user_name_2>")
        api.add_resource(GetHotelRecommendation, "/hotel_recommendation/<food_name>")

        # Start the server
        app.run(host='0.0.0.0', port=7005, debug=True)
    except Exception as e:
        raise Exception("Error while staring the program:"+str(e))