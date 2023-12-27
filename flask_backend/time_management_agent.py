import datetime
import random
from uagents import Agent, Context
import requests

class TimeManagementAgent(Agent):
    def __init__(self, name, seed):
        super().__init__(name=name, seed=seed)
        self.user_preferences = {}
        self.completed_tasks = []
        self.scheduled_events = []
        self.motivation_factor = 1.0

    async def handle_event(self, event, ctx: Context):
        if event == "startup":
            await self.collect_user_preferences(ctx)
            await self.suggest_time_management_strategy(ctx)
            await self.schedule_events(ctx)

    async def collect_user_preferences(self, ctx: Context):
        ctx.logger.info("Collecting user preferences for time management.")

        self.user_preferences["urgent_tasks"] = self.collect_tasks("urgent tasks", ctx)
        self.user_preferences["important_tasks"] = self.collect_tasks("important tasks", ctx)
        self.user_preferences["routine_tasks"] = self.collect_tasks("routine tasks", ctx)
        self.user_preferences["leisure_activities"] = self.collect_tasks("leisure activities", ctx)

    def collect_tasks(self, category, ctx: Context):
        tasks = []
        ctx.logger.info(f"Please provide {category}. Enter each task on a new line. Type 'done' when finished.")
        while True:
            task_input = input(f"{category.capitalize()}: ")
            if task_input.lower() == 'done':
                break
            tasks.append(task_input)
        return tasks

    async def suggest_time_management_strategy(self, ctx: Context):
        ctx.logger.info("Suggesting time management strategy based on user preferences and external factors.")

        weather_conditions = self.get_weather_conditions(ctx)
        ctx.logger.info(f"Weather conditions: {weather_conditions}")

        task_deadline = datetime.datetime.now() + datetime.timedelta(days=2)
        prioritized_tasks = self._prioritize_tasks()
        categorized_tasks = self._categorize_tasks(prioritized_tasks)
        suggested_tasks = self._suggest_tasks(categorized_tasks, task_deadline, weather_conditions)
        motivated_tasks = self._apply_motivation_factor(suggested_tasks)

        if motivated_tasks:
            ctx.logger.info(f"Suggested tasks: {', '.join(motivated_tasks)}")
            await self.simulate_user_feedback(ctx, motivated_tasks)
        else:
            ctx.logger.info("No specific tasks suggested for this time block.")

    async def schedule_events(self, ctx: Context):
        ctx.logger.info("Scheduling events.")

        for event_summary, event_start in self._generate_scheduled_events():
            await ctx.request("calendar_agent", action="schedule_event", event_summary=event_summary, event_start=event_start)

    def _generate_scheduled_events(self):
        for _ in range(3):
            event_summary = f"Meeting with {random.choice(['Client', 'Team', 'Mentor'])}"
            event_start = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 7), hours=random.randint(9, 18))
            yield event_summary, event_start

    def get_weather_conditions(self, ctx: Context):
        api_key = 'd486604013460d5d1888d50056c277f3'  # Replace with a valid API key from a weather service provider
        city = 'Mumbai'
        weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=d486604013460d5d1888d50056c277f3'
        
        try:
            response = requests.get(weather_api_url)
            response.raise_for_status()
            weather_data = response.json()

            if 'weather' in weather_data and len(weather_data['weather']) > 0:
                weather_condition = weather_data['weather'][0]['description']
                return weather_condition
        except requests.RequestException as e:
            ctx.logger.warning(f"Failed to fetch weather data: {e}")

        return 'Unknown'

    def _prioritize_tasks(self):
        prioritized_tasks = []
        prioritized_tasks.extend(self.user_preferences.get("urgent_tasks", []))
        prioritized_tasks.extend(self.user_preferences.get("important_tasks", []))
        prioritized_tasks.extend(self.user_preferences.get("routine_tasks", []))
        prioritized_tasks.extend(self.user_preferences.get("leisure_activities", []))
        return prioritized_tasks

    def _categorize_tasks(self, tasks):
        categorized_tasks = {
            "urgent_important": [],
            "urgent_not_important": [],
            "not_urgent_important": [],
            "not_urgent_not_important": [],
        }

        for task in tasks:
            if task in self.user_preferences.get("urgent_tasks", []):
                categorized_tasks["urgent_important"].append(task)
            elif task in self.user_preferences.get("important_tasks", []):
                categorized_tasks["not_urgent_important"].append(task)
            elif task in self.user_preferences.get("routine_tasks", []):
                categorized_tasks["not_urgent_not_important"].append(task)
            elif task in self.user_preferences.get("leisure_activities", []):
                categorized_tasks["not_urgent_not_important"].append(task)

        return categorized_tasks

    def _suggest_tasks(self, categorized_tasks, deadline, weather_conditions):
        suggested_tasks = []

        for task_category, tasks in categorized_tasks.items():
            if task_category == "urgent_important":
                suggested_tasks.extend(tasks)
            elif task_category == "not_urgent_important":
                if 'rain' in weather_conditions.lower():
                    suggested_tasks.extend(random.sample(tasks, k=min(len(tasks), 2)))
            elif task_category == "not_urgent_not_important":
                current_hour = datetime.datetime.now().hour
                if 8 <= current_hour < 18:
                    suggested_tasks.extend(random.sample(tasks, k=min(len(tasks), 2)))
                else:
                    suggested_tasks.extend(random.sample(tasks, k=min(len(tasks), 3)))

        approaching_deadline_tasks = self._get_approaching_deadline_tasks(deadline)
        suggested_tasks.extend(approaching_deadline_tasks)

        return suggested_tasks

    def _get_approaching_deadline_tasks(self, deadline):
        approaching_deadline_tasks = []
        for task in self.user_preferences.get("urgent_tasks", []):
            days_until_deadline = (deadline - datetime.datetime.now()).days
            if days_until_deadline < 3:
                approaching_deadline_tasks.append(task)
        return approaching_deadline_tasks

    def _apply_motivation_factor(self, tasks):
        motivated_tasks = []
        for task in tasks:
            if "urgent" in task.lower():
                motivation_factor = random.uniform(1.0, 1.5)
            elif "important" in task.lower():
                motivation_factor = random.uniform(0.8, 1.3)
            else:
                motivation_factor = random.uniform(0.5, 1.0)

            if random.uniform(0, 1) < motivation_factor * self.motivation_factor:
                motivated_tasks.append(task)

        return motivated_tasks

    async def simulate_user_feedback(self, ctx: Context, tasks):
        ctx.logger.info("Simulating user feedback for suggested tasks.")
        
        for task in tasks:
            feedback = input(f"Do you want to mark '{task}' as completed? (yes/no): ")
            if feedback.lower() == 'yes':
                self.completed_tasks.append(task)
                ctx.logger.info(f"Marked '{task}' as completed.")
        
        ctx.logger.info("User feedback simulation completed.")

if __name__ == "__main__":
    time_management_agent = TimeManagementAgent(name="time_management_agent", seed="time_management_seed")
    time_management_agent.run()
