from fastapi import FastAPI, status, Body


app = FastAPI()


# Database
db = []

# Our Routes for expenses
@app.get("/get_expenses")
def get_expenses():
    return {
        "status":status.HTTP_200_OK,
        "data":db
    }

@app.post("/add_expense")
def add_expense(description:str = Body(min_length=2), amount:int = Body()):
    new_item = {
        "id":db.__len__() + 1,
        "description":description,
        "amount":amount
    }
    db.append(new_item)

    return {
          "status":status.HTTP_201_CREATED,
          "data":new_item
    }

@app.get("/get_expense_by_id")
def get_expense_by_id(id:int):

    for item in db:
        if item["id"] == id:
            return {
                "status":status.HTTP_200_OK,
                "data":item
            }
        
    return {
        "status":status.HTTP_404_NOT_FOUND,
        "details":"Item Not Found"
    }

@app.put("/edit_expense_by_id")
def edit_expense_by_id(id:int = Body(), description:str = Body(min_length=2), amount:int = Body() ):

    for item in db:
        if item["id"] == id:
            new_item = {
                "id":id,
                "description":description,
                "amount":amount
            }

            item = new_item

            return {
                "status":status.HTTP_201_CREATED,
                "details":"The item has been updated!"
            }

    return {
        "status":status.HTTP_404_NOT_FOUND,
        "details":"Item Not Found"
    }

@app.delete("/remove_expense_by_id")
def remove_expense_by_id(id:int):

    for item in db:
        if item["id"] == id:
            db.remove(item)
        return{
            "status":status.HTTP_200_OK
        }

    return {
        "status":status.HTTP_404_NOT_FOUND,
        "details":"Item Not Found"
    }

