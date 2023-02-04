const GET = "GET", POST = "POST", DELETE = "DELETE", PATCH = "PATCH"
const host = "http://localhost:5000"

// todo: create a function to create a todo
function create_todo() {
    fetch(`${host}/`, {
        method: POST, headers: {
            "Content-Type": "application/json"
        }, body: JSON.stringify({
            "title": "default title", "description": "default description"
        })
    }).then(result => {
        if (result.ok) {
            alert("Todo Added Successfully.")
            list_todos()
        }
    })
}

// todo: create a function to update a todo
function update_todo(event) {
    const todo = event.currentTarget.todo
    console.log(todo)
}

function delete_todo(event) {
    const todo = event.currentTarget.todo
    if (confirm("Are you sure you want to delete this todo?")) {
        fetch(`${host}/${todo.id}`, {
            method: DELETE
        }).then(res => {
            if (res.status === 200) {
                alert("Todo Deleted Successfully.")
                list_todos()
            }
        })
    }
}

function list_todos() {
    fetch(`${host}`, {
        method: GET
    })
        .then(result => result.json())
        .then(todos => {
            if (todos.length > 0) {
                let todos_div = document.getElementById("todos")
                todos_div.innerHTML = ""
                todos_div.className = "text-center"

                let table = document.createElement("table")
                table.className = "table table-hover center"

                const header = table.createTHead()
                let headerRow = header.insertRow()
                headerRow.insertCell().innerHTML = "<b>id</b>"
                headerRow.insertCell().innerHTML = "<b>title</b>"
                headerRow.insertCell().innerHTML = "<b>description</b>"

                let optionsCell = headerRow.insertCell()
                optionsCell.colSpan = 2
                optionsCell.innerHTML = "<b>Options</b>"

                let body = table.createTBody()
                for (let todo of todos) {
                    const bodyRow = body.insertRow()
                    let bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.id
                    bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.title
                    bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.description

                    // the edit button
                    bodyRowCell = bodyRow.insertCell()
                    const editBtn = document.createElement("button")
                    editBtn.className = "btn btn-outline-info"
                    editBtn.innerText = "Edit"
                    editBtn.todo = todo
                    // todo: here when click on edit button, show the edit dialog. editBtn.onclick
                    editBtn.addEventListener("click", update_todo, false)
                    bodyRowCell.append(editBtn)

                    // the delete button
                    bodyRowCell = bodyRow.insertCell()
                    const deleteBtn = document.createElement("button")
                    deleteBtn.className = "btn btn-outline-danger"
                    deleteBtn.innerText = "Delete"
                    deleteBtn.todo = todo
                    deleteBtn.addEventListener("click", delete_todo, false)
                    bodyRowCell.append(deleteBtn)

                    bodyRow.append(bodyRowCell)
                    body.append(bodyRow)
                }
                table.append(body)
                todos_div.append(table)
            } else {
                let todos_div = document.getElementById("todos")
                todos_div.innerHTML = ""
            }
        }).catch(error => {
        console.log(error)
    })
}

window.onload = list_todos
document.getElementById("addTodo").addEventListener("click", create_todo)
