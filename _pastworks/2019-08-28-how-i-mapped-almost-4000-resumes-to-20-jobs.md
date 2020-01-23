---
layout: post
title: "I mapped almost 5000 CVs to 20 jobs"
author: "Dipesh"
---

## The Problem

After some works in text processing and NLP, I had this client who needed to map around 5k CVs to the jobs. Those CVs were related to ship crew jobs, like Captain, Chef, Engineer, etc. So, it was a tough ask to understand the domain, and create a proper dataset for the problem. Also, because this project demanded to be end-to-end, from design to deployment, there were quite a lot of challanges I faced during it's development.

## The Solution

The first thing I decided was to create the backend using django. It's ORM feature and ease of use made it a no-brainer. I quickly came up with the models as below:

``` python

class CV(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_from_doc = models.TextField(blank=True, null=True)
    drive_url = models.CharField(max_length=255, blank=True, null=True)

class Candidate(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

class Match(models.Model):
    candidate = models.ForeignKey(Candidate, blank=True, null=True, on_delete=models.CASCADE, related_name='candidate')
    job = models.ForeignKey(Job, blank=True, null=True, on_delete = models.CASCADE, related_name='job')
    score = models.FloatField(null=True, blank=True, default=0.0)
    top_keywords = models.TextField(null=True, blank=True)
    current_position = models.ForeignKey(Job, blank=True, null=True, on_delete=models.CASCADE, related_name='current_job')
    email = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=50)
    nationality = models.CharField(null=True, blank=True, max_length=50)
    notes = models.TextField(null=True, blank=True)
    salary = models.CharField(null=True, blank=True, max_length=50)
    qualifications = models.TextField(null=True, blank=True)

```

These models were designed keeping in mind that that the client may make feature requests regarding the models. These ones are pretty straightforward, CV model for the CV doc, Candidate for the applicant, and Match model has more importance than others here because the client wanted me to display score and candidate details in the match page of the admin.

I, then started with the big picture on what the components of the project would look like. I quickly came up with these:  


### Parsing the CV docs and Text Processing  


Yes, text extraction has come a long way these days. But the struggle was real when I had to deal with too graphic or styled texts. My tool of choice for text extraction in such use cases is Apache Tika. It is fast, scalable and works like a charm.

``` python
form tika import parser
file_data = parser.from_file(file_path)
```

Another thing to note is that there were serveral CVs for the same candidate. So, I had to filter them as well.

``` python
def filter_cvs(cv_folder):
    """
    takes in the cv_folder 
    returns only the cv files (pdf, or docx, or ...)
    """
    files = []
    for (dirpath, dirnames, filenames) in os.walk(cv_folder):
        files.extend(filenames)
    print(len(files))
    files_with_duplicates = []
    files_without_duplicates = []
    for i in files:
        f = i.split(".")
        if "CV" in i or "cv" in i:
            if not any(f[0] in j for j in files_without_duplicates):
                files_without_duplicates.append(os.getcwd() + "/all_candidates/" + i)
    print(len(files_without_duplicates))
    return files_without_duplicates
```

I also created a class to capture important features from the CV like nationality, phone, email etc.using regex.

``` python
class Rule():
    '''
    Rule class containing several rules to extract 
    several information from the CV
    '''
    def __init__(self, cv):
        self.cv = cv

    def find_email(self, ):
        regex = r"\S+@\S+"
        cv = self.cv
        if cv.text_from_doc is not None:
            email = re.findall(regex, cv.text_from_doc)
            if len(email)>0:
                return email[0]
        return ''
        
    def find_phone(self, ):
        regex = r"\+\d+(?:[-? \)]+\d+)+"
        cv = self.cv
        if cv.text_from_doc is not None:
            phone = re.findall(regex, cv.text_from_doc)
            if len(phone)>0:
                if len(phone[0])>9:
                    return phone[0]
            elif len(phone)>1:
                if len(phone[1])>9:
                    return phone[1]
        return ''
        
    def nationality(self, ):
        cv = self.cv 
        regex = r"citizenship[:\s*\t*]*\w+"
        regex = re.compile(regex)
        if cv.text_from_doc is not None:
            text = cv.text_from_doc.lower().replace('\t', ' ')
            nationality = re.findall(regex, text)
            if len(nationality)>0:
                return nationality[0]
        return ''

    def __str__(self):
        return self.cv
```

### Creating dataset for around 20 job descriptions  

This was the biggest challenge for me because I had almost zero knowledge of the domain. Little help from the client made the situation worse as I had to work my way around finding enough text from the web manually to create enough dataset that could bring satisfactory results.
After a lot of iterations, I opted for this :

``` python
import pandas as pd

chef = ['chef', 'guest', 'health', 'sanitation', 'cook', 'cooking', 'allergy', 'allergies', 'storage']
eto = ['electronic', 'computer', 'audio', 'visual', 'radio', 'radar', 'telephone', 'satellite', 'navigation', 'computer', 'dvd']
...
electrician = ['electrician', 'electrical', 'electronic', 'satellite', 'navigation', 'computer', 'tv', 'dvd']
avit = ['av', 'it', 'audio', 'visual', 'radio', 'radar', 'telephone', 'satellite', 'navigation', 'computer', 'tv', 'dvd']

dict_of_jobs = {}
dict_of_jobs['chef'] = chef
dict_of_jobs['eto'] = eto
dict_of_jobs['electrician'] = electrician
dict_of_jobs['avit'] = avit

df_jd = pd.DataFrame()
for i in dict_of_jobs:
    df = pd.DataFrame.from_dict({i:pd.Series(dict_of_jobs[i])})
    df_jd = pd.concat([df_jd, df], axis=1)
```

Above dataset misses some data, but the general idea is similar. To come to this, I used NLP methods like tokenization, POS tagging, lemmatization etc. I will link the repo to all the code at the end. Feel free to check it out.

### Classifying the CV docs into jobs

Now, with the dataset in hand, I was ready to test it. Although skeptic about my dataset, I tried it out with the famous spacy NLP PhraseMatcher. I love spacy and try to use if for almost all of my NLP tasks. The results here were satisfactory enough for my liking. The client was still not totally satisfied with the results, but with the limited budget and resources,I thought it was what I could do.

### Scoring

For the most important component of the product, I used spacy's PhraseMatcher from the vocab of keywords. Then, I simply assigned keywords and their repetition against each candidate, and used these counts for the score. Assigning scores was then just the matter of getting the maximum counts in a candidate for each job.

``` python
def create_profile(text, candi_name):
    text = str(text)
    # Create CV Dataset
    text = text.lower()
    df_jd = jd.df_jd
    total_dataset = {}
    for job in df_jd:
        temp_keys = []
        for key in df_jd[job]:
            if key is not np.nan:
                temp_keys.append(key)
        total_dataset[job] = [nlp(text) for text in temp_keys]
    
    matcher = PhraseMatcher(nlp.vocab)
    for job in total_dataset:
        matcher.add(job, None, *total_dataset[job])
    
    doc = nlp(text)
    
    d = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id] # get the unicode ID
        span = doc[start : end] # get the matched slice of the doc
        d.append((rule_id, span.text))
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())

    # Convert string of keywords to df
    df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis = 1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    name = pd.read_csv(StringIO(candi_name), names = ['Candidate Name'])
    dataf = pd.concat((name['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']), axis=1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    return dataf

def create_score():
    df = pd.read_csv('sample.csv', index_col=False)
    final_db = []
    for i in range(df.shape[0]):
        score_dict = {}
        series = df.loc[i]
        max_score = max(series[1:])
        keys = df.loc[i].keys()
        candi = series['Candidate Name']
        for j in keys:
            if df.loc[i][j] == max_score:
                score_dict['candidate'] = candi
                score_dict['score'] = max_score
                score_dict['job'] = j 
                final_db.append(score_dict)
    return final_db
```

### Deploying the product  

Finally, I had to deploy the product as the client wanted to view it by himself with all the dashboard and frontend features. I used Django for that specific reason. For deployment, I opted for 1GB RAM Digitalocean instance, and it worked quite well.
Another thing I added as a bonus was the ability to store the CVs to google drive on the fly. Means not only all the 5000 CVs were stored in google drive, but also a new CV upload feature was created that would capture text using Tika on the fly and store the CV on google drive. The code to this is again in the repo.
Although, I finished the upload feature, what I would still like is the ability to assign scores and the respective job for the CV. Hopefully, that will be covered in next phase.

## Further Improvement

As an individual contractor, It was a project I handled without much support from the client. Thus, there are still several rooms for improvement. These are the things I would still like to work on in the future:

1. Use a modern deep learning method (word2vec or transformers for the classification)
2. Complete the online upload feature, so that the uploaded CV gets a score on the fly

If possible, I would also like to work on a different domain of this same problem. So, I am happy to work with clients who are looking to automate their resume-job workflow.

Please find the code in this repo: [https://github.com/dipespandey/cvjd](https://github.com/dipespandey/cvjd)

Thanks for reading till the end. As always, suggestions are welcome. Cheers!
