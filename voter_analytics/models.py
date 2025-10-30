# models.py
# author: Mia Batista 
# model file that stores the data of registered voters

from django.db import models
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    '''
    model that stores/represents the data of registered voters 
    in the town of Newton, MA.
    '''

    # core identity
    last_name = models.TextField()
    first_name = models.TextField()
    
    
    # location things
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)  
    zip_code = models.TextField(blank=True)

    # dates
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)

    # misc
    party = models.CharField(max_length=2, blank=True)  
    precinct = models.CharField(max_length=16, blank=True)

    # election participation (booleans)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''string representation of the voter class'''
        return f'Name: {self.last_name}, {self.first_name} , Party: {self.party or "?"} , VoterScore: {self.voter_score}'

    def parse_date(s):
        '''converts the string into a python date object to make it easier late on!'''
        s = s.strip()
        if not s:
            return None 
        try:
            return datetime.strptime(s,"%Y-%m-%d").date()
        except:
            None

    def parse_bool(s):
        '''converts the strings in the CSV to actual True and False'''
        s = s.strip().upper()
        if s == "TRUE":
            return True
        else:
            return False

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = '/Users/miajolie/Desktop/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:

        fields = line.split(',')
       
        try:
            # create a new instance of Voter object with this record from CSV
            # STILL NEED TO FIX THE FIELDS HERE
            result = Voter(
                            first_name=fields[2],
                            last_name=fields[1],
                            
                            street_number=fields[3],
                            street_name = fields[4],
                            apartment_number = fields[5],
                            zip_code = fields[6],
                            
                            date_of_birth = Voter.parse_date(fields[7]),
                            date_of_registration = Voter.parse_date(fields[8]),
 
                            party = fields[9],
                            precinct = fields[10],
                            v20state = Voter.parse_bool(fields[11]),
                        
                            v21town = Voter.parse_bool(fields[12]),
                            v21primary = Voter.parse_bool(fields[13]),
                            v22general = Voter.parse_bool(fields[14]),
                            v23town = Voter.parse_bool(fields[15]),
                            voter_score = int(fields[16]),
                        )
         
 
            result.save() # commit to database
            print(f'Created result: {result}')
            
        # except:
        #     print(f"Skipped: {fields}")
        except Exception as e:
            print(f"Skipped: {fields} | error: {e}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')
