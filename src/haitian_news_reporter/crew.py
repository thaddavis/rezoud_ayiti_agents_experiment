from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from crewai.tools import (
#     WebsiteSearchTool
# )

from pydantic import BaseModel

from crewai_tools import ScrapeWebsiteTool

# Uncomment the following line to use an example of a custom tool
# from haitian_news_reporter.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

scrap_web_tool = ScrapeWebsiteTool()

class NewsResult(BaseModel):
	headline: str
	description: str
	tags: list[str]

class NewsResults(BaseModel):
	results: list[NewsResult]

@CrewBase
class HaitianNewsReporterCrew():
	"""HaitianNewsReporter crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			tools=[scrap_web_tool],
			verbose=True
		)

	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=NewsResults,
			output_file='report.json'
		)

	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the HaitianNewsReporter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)