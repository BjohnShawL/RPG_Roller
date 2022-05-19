import logging
from random import randint
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    def handle_single_roll(sides :int, modifier: int = 0, neg: bool = False):
        result = randint(1,sides)
        modded = result + modifier if not neg else result - modifier
        if modifier > 0 :
            detail =f"{result} {'+' if not neg else '-'} {modifier }"
        else:
            detail = f"{result}"
        result_dict["sum"]+=modded
        if detail:
            result_dict["detail"].append(detail)

    results_list=[]
    try:
        req_body = req.get_json()
    except ValueError:
            return func.HttpResponse("Failed to get json", 500)
    else:
        dice_list =  req_body.get("dice")
        for dice in dice_list:
            quantity = dice.get("number")
            sides = dice.get("sides")
            modifier = dice.get("mod")
            neg = dice.get("neg",False)
            result_dict = {"sum":0, "detail":[]}
            for _ in range(quantity):
                handle_single_roll(sides=sides,modifier=modifier, neg=neg)
            results_list.append(result_dict)
        _body= json.dumps(results_list)
        return func.HttpResponse(body=_body, status_code=200)
