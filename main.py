import math as maths
from operator import add, sub, mul, truediv
from typing import Callable

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, PrivateAttr


operators = {
    "add": add,
    "subtract": sub,
    "multiply": mul,
    "divide": truediv
}


class Calculation(BaseModel):
    operation: str
    left: float
    right: float
    precision: int = 2

    def get_result(self):
        op = operators.get(self.operation)

        if op is None:
            raise ValueError("Invalid OP, {self.operation}")

        return round(op(self.left, self.right), self.precision)


class CalculationResult(BaseModel):
    operation: str
    left: float
    right: float
    precision: int
    result: float


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "PyDis is the BestDis"}


@app.get("/calculate", response_model=CalculationResult)
def calculate(calculation: Calculation):

    try:
        result = calculation.get_result()

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The operator {calculation.operation} is not valid. Choose one of {', '.join(operators.keys())}",
        )

    response_body = CalculationResult(result=result, **calculation.dict())

    return response_body
