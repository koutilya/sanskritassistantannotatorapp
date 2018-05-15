from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from . import models,forms,codeforline
from .models import Sentences,WordOptions,Wordsinsentence
from .tables import WordOptionsTable,SentencesTable,WordsinsentenceTable
import json 



# from datatableview.views import DatatableView

from django_datatables_view.base_datatable_view import BaseDatatableView
# Create your views here.

def index(request) :

	return render(request,'sanskritannotator/index.html',{})


def lineview(request) :
	return render(request,'sanskritannotator/index.html',{})


# def wordtableview(request) :

# 	wordsdata = WordOptions.objects.all()

# 	return render(request,'sanskritannotator/wordtable.html',{'wordsdata' : wordsdata})

# class ZeroConfigurationDatatableView(BaseDatatableView):
#     model = WordOptions
#     columns = ['word', 'lemma', 'morph', 'aux_info', 'pre_verb']
#     order_columns = ['word', 'lemma', 'morph']


def wordtableview(request) :

	tabledata = WordOptionsTable(WordOptions.objects.all())

	return render(request,'sanskritannotator/tables.html',{'tabledata' : tabledata})
		
def sentenceview(request) :

	tabledata = SentencesTable(Sentences.objects.all())

	return render(request,'sanskritannotator/tables.html',{'tabledata' : tabledata})

def wordsinsentenceview(request) :

	tabledata = WordsinsentenceTable(Wordsinsentence.objects.all())

	return render(request,'sanskritannotator/tables.html',{'tabledata' : tabledata})


def get_dragdata(request):
	if request.is_ajax() :
		if request.method == 'POST':
			sent_id = json.loads(request.POST['sentid'])
			Sentence1 = Sentences.objects.get(id = sent_id)
			wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
			data  = codeforline.getsentwordtree(sent_id);
			print(data)
			return HttpResponse(data)
	else:
		raise Http404

def save_dragdata(request):
	if request.is_ajax() :
		if request.method == 'POST':
			# print(request)
			# dragdata = request.session.get('dd')
			wp = json.loads(request.POST['wp'])
			wc = json.loads(request.POST['wc'])
			wr = json.loads(request.POST['wr'])
			sent_id = json.loads(request.POST['sentid'])
			Sentence1 = Sentences.objects.get(id = sent_id)

			wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)

			for w in wordsdata :
				try:
					w.isSelected = False
					w.isEliminated = True
					w.parent = -1
					w.relation = ''
					w.children = ''

					w.save()
				except Exception as e:
					print("wordsdata updated in ajex save_dragdata:selection elimination ")
					print(e)
				
			for i in wp:
				
				try:
					w = WordOptions.objects.get(id = i)
					w.parent = int(wp[i])
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wp ")
					print(e)
			for i in wr:
				
				try:
					w = WordOptions.objects.get(id = i)
					w.relation = wr[i]
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wr ")
					print(e)
			for i in wc:
				
				try:
					w = WordOptions.objects.get(id = i)
					w.children = w.children+wc[i]
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wc ")
					print(e)
			

			# print(request.POST['wc'])
			# context['dragdata'] = dragdata	
			return HttpResponse("Success!")
	else:
		raise Http404




def presentdataview(request) :

	if request.method == "POST" :
		Inputlineform = forms.inputlineform(request.POST)

		# print(request.POST.get("checkbox")=='on')
		# if request.POST.get("checkbox")=='on' :
		# 	saveline = True
		# else :
		# 	saveline = False

		saveline = True

		if Inputlineform.is_valid():
			print('form is is_valid')

			try:

				Sentence = Sentences(
										line = Inputlineform.cleaned_data['line'],
										linetype = Inputlineform.cleaned_data['linetype'],

							)
				

				if not codeforline.checksent(Sentence) :
					
					df = codeforline.getdatafromsite(Sentence)
					if saveline :
						Sentence.save()
						codeforline.savedatafromsite(df,Sentence)
						print("Adding Sentences data to Database \n\n")

				if  codeforline.checksent(Sentence) :
					Sentence1 = Sentences.objects.get(line = Sentence.line,linetype=Sentence.linetype)

					wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
					words = Sentence1.line.split(' ')
					chunknum = {}
					c = 0
					for word in words :
						c = c+1
						chunknum[word] = c
					
					# request.session['wordsdata']=wordsdata
					# request.session['words']=words
					# request.session['chunknum']=chunknum

					sent_id = Sentence1.id
					pos = 0
					# context = {'wordsdata' : wordsdata,'words' :words,'chunknum' : chunknum,'sentid':sent_id,'l10':range(10),'pos':pos,}
					context  = codeforline.contestofwordsdata(sent_id)
					return render(request,'sanskritannotator/presentdata.html',context)
				else :
					wordsdata = codeforline.worddataofsentence(df,Sentence)
					
					return render(request,'sanskritannotator/presentdata.html',{'wordsdata' : wordsdata,'words' : Sentence.line.split(' ') , 	})

				
			except Exception as e:  

				print("Sentence not inserted : ")
				print(e)
				# print(codeforline.contestofwordsdata(sent_id))


		Sentences1 = Sentences.objects.all()
		for s in Sentences1 :
		 sent_id = s.id
		 break

		return render(request,'sanskritannotator/presentdata.html',{'sentid':sent_id})
	else :
		
		Sentence1 = Sentences.objects.get(id = request.session.get('sent_id'))

		wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
		words = Sentence1.line.split(' ')
		chunknum = {}
		c = 0
		for word in words :
			c = c+1
			chunknum[word] = c
		sent_id = Sentence1.id
		pos = 0
		# context = {'wordsdata' : wordsdata,'words' :words,'chunknum' : chunknum,'sentid':sent_id,'l10':range(10),'pos':pos,	}
		context = codeforline.contestofwordsdata(sent_id)
		return render(request,'sanskritannotator/presentdata.html',context)
	
def select_wordoptionview(request,sent_id,wordoption_id) :
	wo = WordOptions.objects.get(id=wordoption_id)
	wo.isSelected = True
	request.session['sent_id'] = sent_id
	wo.save()
	return redirect('sanskritannotator:presentdataview')			

def eliminate_wordoptionview(request,sent_id,wordoption_id) :
	wo = WordOptions.objects.get(id=wordoption_id)
	wo.isEliminated = True
	wo.save()
	request.session['sent_id'] = sent_id

	return redirect('sanskritannotator:presentdataview')	

def reset_allselectionview(request,sent_id)	:
	Sentence1 = Sentences.objects.get(id = sent_id)
	wordsdata = WordOptions.objects.all().filter(sentence = Sentence1	)
	for wo in wordsdata :
		wo.isSelected = False
		wo.isEliminated=False

		wo.parent = -1
		wo.relation = ''
		wo.children = ''
		wo.save()
	request.session['sent_id'] = sent_id

	return redirect('sanskritannotator:presentdataview')	