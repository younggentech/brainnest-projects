const GET = "GET", POST = "POST", DELETE = "DELETE", PATCH = "PATCH"
const host = "http://localhost:5050"


const modal = new bootstrap.Modal(document.getElementById("staticBackdrop"));

function create_todo() {
    const title = document.getElementById("todoTitle").value
    const description = document.getElementById("todoDescription").value
    fetch(`${host}/`, {
        method: POST, headers: {
            "Content-Type": "application/json"
        }, body: JSON.stringify({
            "title": `${title}`, "description": `${description}`
        })
    }).then(result => {
        if (result.ok) {
            alert("Todo Added Successfully.")
            modal.toggle();
            list_todos()
        }
    })
}

function update_todo(event) {
    const todo = event.currentTarget.todo
    const title = document.getElementById("todoTitle").value
    const description = document.getElementById("todoDescription").value
    fetch(`${host}/${todo.id}`, {
        method: PATCH, headers: {
            "Content-Type": "application/json"
        }, body: JSON.stringify({
            "title": `${title}`, "description": `${description}`
        })
    }).then(result => {
        if (result.ok) {
            alert("Todo Updated Successfully.")
            modal.toggle();
            list_todos()
        }
    })
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


function complete_todo(todoID) {
    fetch(`${host}/toggle/${todoID}`, {
        method: PATCH
    }).then(result => {
        if (result.ok) {
            list_todos()
        }
    })
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
                headerRow.insertCell().innerHTML = "<b>completed</b>"

                let optionsCell = headerRow.insertCell()
                optionsCell.colSpan = 3
                optionsCell.innerHTML = "<b>Options</b>"

                let body = table.createTBody()
                for (let todo of todos) {
                    const bodyRow = body.insertRow()
                    if (todo.completed) bodyRow.style.textDecoration = "line-through"
                    let bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.id
                    bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.title
                    bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = todo.description
                    bodyRowCell = bodyRow.insertCell()
                    bodyRowCell.innerHTML = `<input type="checkbox" ${todo.completed ? "checked" : ""} name="todo${todo.id}" id="todo${todo.id}" onclick="complete_todo(${todo.id})">`


                    // the edit button
                    bodyRowCell = bodyRow.insertCell()
                    const editBtn = document.createElement("button")
                    editBtn.className = "btn btn-outline-info"
                    editBtn.innerText = "Edit"
                    // todo: here when click on edit button, show the edit dialog. editBtn.onclick
                    editBtn.addEventListener("click", () => {
                        document.getElementById("staticBackdropLabel").innerText = "Edit Todo";
                        document.getElementById("todoTitle").value = todo.title
                        document.getElementById("todoDescription").value = todo.description
                        const btn = document.getElementById("saveTodo")
                        btn.innerText = "Update"
                        btn.removeEventListener("click", create_todo)
                        btn.todo = todo
                        btn.addEventListener("click", update_todo)
                        modal.toggle();
                    }, false)
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
document.getElementById("addTodo").addEventListener("click", () => {
    document.getElementById("saveTodo").removeEventListener("click", update_todo);
    document.getElementById("staticBackdropLabel").innerText = "Add New Todo";
    document.getElementById("todoTitle").value = ""
    document.getElementById("todoDescription").value = ""
    document.getElementById("saveTodo").value = "Save"
    document.getElementById("saveTodo").addEventListener("click", create_todo);
    modal.toggle();
})