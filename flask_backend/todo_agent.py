from uagents import Agent, Context
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
from datetime import datetime, timedelta
import schedule
import time

class TodoAgent(Agent):
    def __init__(self, name, seed):
        super().__init__(name=name, seed=seed)
        self.todos = []

    @property
    def remaining_tasks(self, todo_name):
        todo = next((todo for todo in self.todos if todo["name"] == todo_name), None)
        if todo:
            return [task for task in todo.get("tasks", []) if not task.get("completed", False)]
        return []

    async def handle_event(self, event, ctx: Context):
        if event == "startup":
            await self.introduce_agent(ctx)
            await self.check_deadlines(ctx)
            schedule.every(2).hours.do(lambda: self.checkup_reminder(ctx))

    async def introduce_agent(self, ctx: Context):
        ctx.logger.info(f"Hello, I'm agent {ctx.name} and my address is {ctx.address}.")

    async def add_todo(self, ctx: Context, todo_name: str, deadline: str):
        creation_time = datetime.now()
        deadline_time = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        todo = {"name": todo_name, "tasks": [], "creation_time": creation_time, "deadline_time": deadline_time}
        self.todos.append(todo)
        ctx.logger.info(f"Todo '{todo_name}' added. Created at: {creation_time}, Deadline: {deadline_time}.")

    async def add_task(self, ctx: Context, todo_name: str, task_name: str):
        todo = next((todo for todo in self.todos if todo["name"] == todo_name), None)
        if todo:
            task = {"name": task_name, "completed": False, "creation_time": datetime.now()}
            todo["tasks"].append(task)
            ctx.logger.info(f"Task '{task_name}' added to Todo '{todo_name}'.")
        else:
            ctx.logger.warning(f"Todo '{todo_name}' not found.")

    async def complete_task(self, ctx: Context, todo_name: str, task_name: str):
        todo = next((todo for todo in self.todos if todo["name"] == todo_name), None)
        if todo:
            for task in todo["tasks"]:
                if task["name"] == task_name:
                    task["completed"] = True
                    ctx.logger.info(f"Task '{task_name}' marked as complete in Todo '{todo_name}'.")
                    return
            ctx.logger.warning(f"Task '{task_name}' not found in Todo '{todo_name}'.")
        else:
            ctx.logger.warning(f"Todo '{todo_name}' not found.")

    async def get_remaining_tasks(self, ctx: Context, todo_name: str):
        remaining = self.remaining_tasks(todo_name)
        if remaining:
            ctx.logger.info(f"Remaining tasks in Todo '{todo_name}': {', '.join(task['name'] for task in remaining)}")
        else:
            ctx.logger.info(f"No remaining tasks in Todo '{todo_name}'.")

    async def check_deadlines(self, ctx: Context):
        current_time = datetime.now()
        for todo in self.todos:
            todo_name = todo["name"]
            deadline_time = todo["deadline_time"]
            if current_time > deadline_time:
                ctx.logger.warning(f"Deadline passed for Todo '{todo_name}'.")
            else:
                time_remaining = deadline_time - current_time
                ctx.logger.info(f"Time remaining for Todo '{todo_name}': {time_remaining}")

    def checkup_reminder(self, ctx: Context):
        for todo in self.todos:
            todo_name = todo["name"]
            for task in todo["tasks"]:
                if not task["completed"]:
                    creation_time = task["creation_time"]
                    elapsed_time = datetime.now() - creation_time
                    if elapsed_time >= timedelta(hours=2):
                        ctx.logger.info(f"Reminder: Checkup for Task '{task['name']}' in Todo '{todo_name}'.")
                    else:
                        ctx.logger.info(f"No checkup reminder needed for Task '{task['name']}' in Todo '{todo_name}'.")

def parse_request_params(path):
    # Parse query parameters from the URL
    query_params = parse_qs(path.split("?", 1)[-1])
    return {key: value[0] for key, value in query_params.items()}

class TodoRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            # Route the request to the agent
            if 'action' in params:
                action = params['action']
                del params['action']

                if action == 'add_todo':
                    appointment.add_todo(ctx=None, todo_name=params['todo_name'], deadline=params['deadline'])
                elif action == 'add_task':
                    appointment.add_task(ctx=None, todo_name=params['todo_name'], task_name=params['task_name'])
                elif action == 'complete_task':
                    appointment.complete_task(ctx=None, todo_name=params['todo_name'], task_name=params['task_name'])
                elif action == 'remaining_tasks':
                    appointment.get_remaining_tasks(ctx=None, todo_name=params['todo_name'])

            self.send_response(200)
            self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

if __name__ == "__main__":
    appointment = TodoAgent(name="appointment", seed="alice recovery phrase")

    # Start the HTTP server to handle requests
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TodoRequestHandler)

    print('INFO: Starting server on http://0.0.0.0:8000 (Press CTRL+C to quit)')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
