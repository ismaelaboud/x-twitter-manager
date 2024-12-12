from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

class SchedulingService:
    def __init__(self):
        # Initialize async scheduler
        self.scheduler = AsyncIOScheduler()
        self.scheduled_jobs: Dict[str, Dict] = {}
    
    def schedule_tweet(self, 
                       tweet_func, 
                       tweet_args: List, 
                       schedule_time: Optional[datetime] = None,
                       interval: Optional[int] = None,
                       job_id: Optional[str] = None):
        """
        Schedule a tweet to be posted
        
        :param tweet_func: Function to post tweet
        :param tweet_args: Arguments for tweet function
        :param schedule_time: Specific time to post
        :param interval: Interval in minutes to repeat
        :param job_id: Unique identifier for the job
        :return: Job ID
        """
        if not job_id:
            job_id = f"tweet_{datetime.now().timestamp()}"
        
        try:
            if schedule_time:
                # Schedule at a specific time
                trigger = DateTrigger(run_date=schedule_time)
                job = self.scheduler.add_job(
                    tweet_func, 
                    trigger, 
                    args=tweet_args, 
                    id=job_id
                )
            elif interval:
                # Schedule with interval
                trigger = IntervalTrigger(minutes=interval)
                job = self.scheduler.add_job(
                    tweet_func, 
                    trigger, 
                    args=tweet_args, 
                    id=job_id
                )
            else:
                raise ValueError("Either schedule_time or interval must be provided")
            
            # Store job details
            self.scheduled_jobs[job_id] = {
                'func': tweet_func,
                'args': tweet_args,
                'schedule_time': schedule_time,
                'interval': interval
            }
            
            return job_id
        except Exception as e:
            print(f"Scheduling error: {e}")
            return None
    
    def cancel_scheduled_tweet(self, job_id: str):
        """
        Cancel a scheduled tweet
        
        :param job_id: ID of job to cancel
        :return: Boolean indicating success
        """
        try:
            self.scheduler.remove_job(job_id)
            del self.scheduled_jobs[job_id]
            return True
        except Exception as e:
            print(f"Error canceling job: {e}")
            return False
    
    def list_scheduled_tweets(self):
        """
        List all scheduled tweets
        
        :return: Dictionary of scheduled jobs
        """
        return {
            job_id: {
                'next_run': job.next_run_time,
                'func_name': job.func.__name__
            } 
            for job_id, job in self.scheduler.get_jobs().items()
        }
    
    def start(self):
        """
        Start the scheduler
        """
        if not self.scheduler.running:
            self.scheduler.start()
    
    def shutdown(self):
        """
        Shutdown the scheduler
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
