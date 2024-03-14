from django.db import models
import os


def file_upload_path(instance, filename):    
    return os.path.join('excel', instance.category.name, filename)

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.name}'

class File(models.Model):
    DEFAULT_CATEGORY_ID = 1  # Assuming the default category ID is 1

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=DEFAULT_CATEGORY_ID)
    title = models.CharField(max_length=200, blank=True) 
    file = models.FileField(upload_to=file_upload_path, blank=True)
    header = models.JSONField(default=dict)   

    def __str__(self):
        return f"{self.category.name} - {self.title}"
    

class Project(models.Model):    
    title = models.CharField(max_length=200, blank=True)    
    excel_files = models.ManyToManyField(File, related_name='files') 

    def __str__(self):
        return self.title
    
class Mapping(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    source_columns = models.JSONField()  # Store list of columns as JSON
    dest = models.CharField(max_length=200, blank= True)
    dest_columns = models.JSONField()    # Store list of columns as JSON
    primary_key = models.JSONField()   # Source column name

    def __str__(self):
        return f'Mapping for {self.project.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Extract data from the mapping
        source_table = self.source
        source_columns = self.source_columns
        dest_columns = self.dest_columns
        primary_key = self.primary_key
        dest_table = self.dest

        print()
        select_clauses = []

        for i in range(len(source_columns)):
            if source_table and source_columns[i]:
                select_clauses.append(f"{source_table}.{source_columns[i]} AS {source_table}_{source_columns[i]}")

        select_clause = ', '.join(select_clauses)

        if dest_table and dest_columns:
            dest_select_clauses = [f"{dest_table}.{dest_columns[i]} AS {dest_table}_{dest_columns[i]}" for i in range(len(dest_columns)) if dest_columns[i]]
            select_clause += ', ' + ', '.join(dest_select_clauses)

        # Constructing the CASE statement for comparison
        case_statements = []
        for i in range(len(source_columns)):
            if source_table and source_columns[i] and dest_table and dest_columns[i]:
                case_statement = f"CASE WHEN {source_table}.{source_columns[i]} IS NOT NULL AND {dest_table}.{dest_columns[i]} IS NOT NULL AND {source_table}.{source_columns[i]} = {dest_table}.{dest_columns[i]} THEN 'true' ELSE 'false' END AS {source_columns[i]}_match"
                case_statements.append(case_statement)
      
        # Constructing the JOIN condition dynamically
        #join_condition = f"INNER JOIN {dest_table} ON {source_table}.{primary_key[0]} = {dest_table}.{source_columns[0]}"

        # Construct join conditions
        count=0
        join_conditions = []
        print(primary_key)
        for key in primary_key:
            for i, source in enumerate(source_columns):
                if key == source:
                    count = count + 1
                    join = f"{source_table}.{source_columns[i]} = {dest_table}.{dest_columns[i]}"
                    join_conditions.append(join)
                    if key != primary_key[-1]:
                        join_conditions.append("AND")
                        print(join_conditions)
                        print('count',count)
                        
        join_condition = " ".join(join_conditions)
        print(count)
        #print(source_columns)
        print(join_condition)
        # Combine join conditions using AND
        join_condition = f"INNER JOIN {dest_table} ON {join_condition}"
        #print(join_condition)
        # Constructing the final SQL query
        sql_query = f"SELECT {select_clause}, {', '.join(case_statements)} FROM {source_table} {join_condition};"
        #print(sql_query)        
        # Get or create SQL instance
        sql_instance, created = Sql.objects.get_or_create(mapping=self)
        sql_instance.sql_query = sql_query
        sql_instance.save()


class Index(models.Model):    
    project = models.OneToOneField(Project, on_delete=models.CASCADE)   
    file = models.FileField(upload_to='index', blank=True) 

    def __str__(self):
        return f'Index for {self.project.title}'

class Sql(models.Model):    
    mapping = models.OneToOneField(Mapping, on_delete=models.CASCADE)   
    sql_query = models.TextField() 

    def __str__(self):
        return f'SQL Query for {self.mapping.project.title}'

class Terminal(models.Model):    
    Project = models.OneToOneField(Project, on_delete=models.CASCADE, blank=True, null= True)   
    sql_query = models.TextField() 

    def __str__(self):
        return f'SQL Query for {self.project.title}'