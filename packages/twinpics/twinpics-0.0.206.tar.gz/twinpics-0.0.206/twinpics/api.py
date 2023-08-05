# Copyright 2019-2020 Alberto Martín Mateos & Niloufar Shoeibi for TWINPICS project
# See LICENSE for details.
# -*- coding: utf-8 -*-

import subprocess
import sys
import warnings
warnings.filterwarnings("ignore")
#---------------------------------------------------------------INSTALLATION---------------------------------------------------------#




##----------------------------------------------IMPORTS---------------------------------------------------------------------------#	
import json
import itertools
import ast
import copy
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import pandas as pd
import numpy as np
import urllib3
import re
import time
import networkx as nx
import requests
import matplotlib.pyplot as plt
import tweepy
from os import path
import os
from datetime import timedelta
from datetime import date, datetime
import community as community_louvain
import leidenalg
import igraph
from igraph import *
from cdlib import algorithms
#from infomap import Infomap
from networkx.algorithms import community
import wordninja
from langdetect import detect
from googletrans import Translator


#---------------------------------------------NLP-Part-------------------------------------------------------------------------------#
from textblob import TextBlob
import nltk
from nltk import RegexpTokenizer
# some small toolkits to download
nltk.download("wordnet")
nltk.download('brown')
nltk.download('punkt')


#----------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def load_file(json_filename):

    data = json.load(json_filename)
    df = pd.DataFrame(data["results"])
    return df

def merge_dataframes(df1, df2):
    df_final = pd.merge(df1, df2, on = ["screen_name"])
    return df_final

#----------------------------------Structure for the graph-----------------------------------------#
def profile_connections (data_tweets):    
    screen_name = []
    screen_name_mention = []
    data = pd.DataFrame()
    data_tweets = data_tweets.rename(columns = {"created_at": "created_at_tw"})
    data_tweets = pd.concat([data_tweets.drop(['user'], axis=1), data_tweets['user'].apply(pd.Series)],
                            axis=1).drop_duplicates().reset_index(drop=True)
    if(data_tweets.empty == False):
        for i in range(len(data_tweets)):
            screen_name.append(data_tweets["screen_name"][i])
            if "@" in (data_tweets["text"][i]):
                split_text = data_tweets["text"][i].split()
                check = "@"
                screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())]
                #Consider that @ is from a email or another words that is not the screen_name
                if not screen_name_mention1:
                    screen_name_mention.append(["Empty"])
                else:
                    if(data_tweets["text"][i].startswith('RT',0)):
                        screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….]", '',str(screen_name_mention1)).split(", ") 
                        screen_name_mention.append([screen_name_mention1[0]])                    
                    else:
                        screen_name_mention.append(re.sub("[\[\]\'\"!@?¿#$:….]", '',str(screen_name_mention1)).split(", "))
            else:
                screen_name_mention.append(["Empty"])
    data["screen_name"] = screen_name    
    data["screen_name_mention"] = screen_name_mention
    # {col:np.repeat(data[col].values, data[lst_col].str.len()) for col in data.columns.difference([lst_col])} --> Las variables diferentes a la objetivo se conservan y se crean varias filas iguales al tamaño de cada
    # una de las listas que hay en cada fila
    # data[lst_col].str.len() --> Longitud de cada lista en cada fila
    # data.columns.difference([lst_col]) -->Columnas diferentes a la evaluada
    # .assign(**{lst_col:np.concatenate(data[lst_col].values)} --> Concatena todos los screen_name y asigna la nueva columna
    # [data.columns.tolist()] --> Dejar el mismo orden de variables
    lst_col = "screen_name_mention"
    data = data[["screen_name","screen_name_mention"]]
	#Create new rows in case of a tweet has different mentions
    data_ext = pd.DataFrame({col:np.repeat(data[col].values, data[lst_col].str.len())for col in data.columns.difference(
        [lst_col])}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]
    data1_ext = pd.DataFrame({'iteration' : data_ext.groupby(data_ext.columns.tolist(),as_index=False).size().sort_values(
                                                                        ascending = False)}).reset_index()
    return data1_ext

def basic_metadata_tweets_extracted (data_tweets, node_list): 
        
    data_tweets = data_tweets.rename(columns = {"created_at": "created_at_tw"})
    df_basic_metadata_tweets_extracted = pd.concat([data_tweets.drop(['user'], axis=1), data_tweets['user'].apply(pd.Series)],
                            axis=1).drop_duplicates().reset_index(drop=True)[["screen_name","followees","followers","statuses_count","url","verified"]]
    df_basic_metadata_tweets_extracted["url"] = "http://www.twitter.com/"+df_basic_metadata_tweets_extracted["screen_name"]

    extract_profiles =[]
    tweets_profiles =  list(df_basic_metadata_tweets_extracted["screen_name"])
    for item in node_list:
      if item not in tweets_profiles:
        extract_profiles.append(item)
          
    return extract_profiles, df_basic_metadata_tweets_extracted

#--------------------------------------Graph building functions---------------------------

def building_node_list(df):

    node_list = pd.DataFrame()
    n = []
    for i in range(len(df)):
        n.append(df['screen_name'].iloc[i])
        n.append(df['screen_name_mention'].iloc[i])
    node_list['screen_name']= n
    node_list = node_list.drop_duplicates()
    node_list = node_list[node_list["screen_name"] !="Empty"].reset_index()
    return list(node_list["screen_name"])
    
    
#---------------------------------Undirect Graph ------------------------------------------------
def node_list_conversion(df_graph):
    nodes = []
    idd=[]
    node_list=pd.DataFrame()
    for i in range(len(df_graph)):
        nodes.append(df_graph['screen_name'].iloc[i])
        nodes.append(df_graph['screen_name_mention'].iloc[i])
    #Create dataframe, drop duplicates and create a new variable called "id"
    node_list['screen_name']= nodes
    node_list=node_list.drop_duplicates(keep='first')
    node_list = node_list[node_list["screen_name"] !="Empty"].reset_index(drop=True)

    for i in range(len(node_list)):
        idd.append(i)
    node_list['id']=idd

    #Create dictionary
    my_dictionary = {node_list["screen_name"][0]: 0}
    for i in range(len(node_list)):
        my_dictionary[str(node_list["screen_name"][i])] = node_list["id"][i]
    my_dictionary["Empty"] = len(node_list)
    df_graph["screen_name_mention_num"] = df_graph["screen_name_mention"]
    df_graph["screen_name_num"] = df_graph["screen_name"]
    for index, row in df_graph.iterrows():
        df_graph.loc[index, 'screen_name_num'] = my_dictionary[row["screen_name"]]
        df_graph.loc[index, 'screen_name_mention_num'] = my_dictionary[row["screen_name_mention"]]
    
    return df_graph, node_list
    


def buildingGraph(df_graph):
    G =nx.Graph()
    for i in range(len(df_graph)):
        G.add_edges_from([(df_graph.screen_name.iloc[i], df_graph.screen_name_mention.iloc[i])])
    return G


def girvanNewman_alg(node_list,df_graph):
    DiG = building_DiGraph(node_list,df_graph,"str")
    communities_generator = community.girvan_newman(DiG)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    communities= sorted(map(sorted, next_level_communities))
    data = pd.DataFrame()
    data["screen_name"]=  communities
    data["community"] = list(range(0,len(communities)))    
    lst_col ="screen_name"
    df_algComu =pd.DataFrame({col:np.repeat(data[col].values, data[lst_col].str.len()) for col in data.columns.difference(
            [lst_col])}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]
    return df_algComu
    
def louvain_alg(node_list,df_graph):
    G = buildingGraph(df_graph)
    partition = community_louvain.best_partition(G)
    l=[]
    for (key,value) in partition.items():
        l.append([key, value])

    df_algComu=pd.DataFrame(data=l,columns= ['screen_name','community'])
    return df_algComu
    
    

def leiden_alg (df_graph):
    df_graph, node_list = node_list_conversion(df_graph)
    DiG = building_DiGraph(list(node_list["id"]),df_graph,"num")
    coms = algorithms.leiden(DiG)
    data = pd.DataFrame()
    data["id"]=  coms.communities
    data["community"] = list(range(0,len(coms.communities)))
    lst_col ="id"
    df_algComu =pd.DataFrame({col:np.repeat(data[col].values, data[lst_col].str.len()) for col in data.columns.difference(
            [lst_col])}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]
    df_algComu = pd.merge(node_list, df_algComu, on=["id"])
    return df_algComu
    
    
def infMap_alg(df_graph):
    # Command line flags can be added as a string to Infomap
    im = Infomap("--two-level --directed")
    df_graph, node_list = structure_leiden(df_graph)
    for i in range(len(df_graph)):
        im.add_link(df_graph['screen_name_num'].iloc[i],df_graph['screen_name_mention_num'].iloc[i])
    # Run the Infomap search algorithm to find optimal modules
    im.run()
    
    nodes=[]
    community=[]
    for node in im.tree:
        if node.is_leaf:
            nodes.append(node.node_id)
            community.append(node.module_id)
    df_algComu=pd.DataFrame()
    df_algComu['id']=nodes
    df_algComu['community']=community
    df_algComu = pd.merge(node_list, df_algComu, on=["id"])  
    
    return df_algComu



def graph_algoritm_selected(df_graph,selection,node_list):

    len_nodeList = len(node_list)
    if(selection ==1): #GirvanNewman
        print("Girvan Newman");
        df_algComu = girvanNewman_alg(node_list,df_graph)
    elif(selection ==2): #Leiden
        print("Leiden");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        df_algComu = leiden_alg(df_graph)
    #elif(selection =="3"):
        #df_algComu = infMap_alg(df_graph)
    else:#default
        if(len_nodeList < 1000):
            df_algComu = girvanNewman_alg(node_list,df_graph)
        else:
            df_algComu = leiden_alg(df_graph)
    
    return df_algComu
        



#------------------------------Directed Graph ---------------------------------------------------
def building_DiGraph(node_list, df_graph, alg_type):
    DiG = nx.DiGraph()
    DiG.add_nodes_from(node_list)
    for i in range(len(df_graph)):
        if alg_type=="str":            
            if(df_graph['screen_name_mention'].iloc[i] !="Empty"):
                DiG.add_edge(df_graph['screen_name'].iloc[i],df_graph['screen_name_mention'].iloc[i])
        else:
            #Second condition for delete empty when we convert screen_name to numbers for specific algorithms
            if(df_graph["screen_name_mention"].iloc[i] != len(node_list)):
                DiG.add_edge(df_graph['screen_name_num'].iloc[i],df_graph['screen_name_mention_num'].iloc[i])
    return DiG
    


def self_loop_iteration_nodes(df):
    df_self_loop_iteration_nodes = pd.DataFrame()
    n = []
    self_loop_iteration = []
    for i in range(len(df)):
        if(df["screen_name"].iloc[i] ==df["screen_name_mention"].iloc[i]):
            n.append(df['screen_name'].iloc[i])
            self_loop_iteration.append(df["iteration"].iloc[i])            
        else:
            n.append(df['screen_name'].iloc[i])
            n.append(df['screen_name_mention'].iloc[i])
            self_loop_iteration.append(0)
            self_loop_iteration.append(0)
    df_self_loop_iteration_nodes['screen_name']= n
    df_self_loop_iteration_nodes['self_loop_iteration']= self_loop_iteration
    df = pd.DataFrame({'times': df_self_loop_iteration_nodes.groupby(["screen_name","self_loop_iteration"]).size().sort_values(
    ascending=False)}).reset_index().drop_duplicates(["screen_name"],keep="first")
    del df["times"]
    return df
	
def DiGraph_visualization (DiG):
    plt.figure(figsize=(30,18))
    nx.draw(DiG, with_labels=True, node_size=10, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=4)
    plt.show()

#---------------------------------Graph features functions ----------------------
def in_degree_centrality(DiG, output):
    l = []
    l = nx.in_degree_centrality(DiG)
    sc = []
    indegcent = []
    for k, v in l.items():
        indegcent.append(v)
        sc.append(k)
    output['in_degree_centrality']=indegcent
    output["screen_name"] = sc    
    return output

def out_degree_centrality(DiG, output):
    l=[]
    l=nx.out_degree_centrality(DiG)
    sc=[]
    outd=[]
    for k, v in l.items():
        outd.append(v)
    output['outdegree_centrality']=outd
    return output

def degree_centrality(DiG,output):
    l=[]
    l=nx.degree_centrality(DiG)
    deg=[]
    for k, v in l.items():
        deg.append(v)
    output['degree_centrality']=deg
    return output

def in_degree(DiG, output):
    indegs=[]
    for i in range(len(list(DiG.nodes))):
        indegs.append(DiG.in_degree(list(DiG.nodes)[i]))
    output['in_degree']=indegs
    return output

def out_degree(DiG, output):
    outdegs=[]
    for i in range(len(list(DiG.nodes))):
        outdegs.append(DiG.out_degree(list(DiG.nodes)[i]))
    output['out_degree']=outdegs
    return output

def degree(DiG, output):
    degs=[]
    for i in range(len(list(DiG.nodes))):
        degs.append(DiG.degree(list(DiG.nodes)[i]))
    output['degree']=degs
    return output

def self_loops(DiG, output):
    SL = list(DiG.nodes_with_selfloops())
    output['self_loop']= False
    l=[]
    for i in range(len(SL)):
        for j in range(len(output)):
            if SL[i]==output['screen_name'].iloc[j]:
                output.self_loop.iloc[j]=True
    return output


def graph_features(DiG,df):

    output = pd.DataFrame()
    output = in_degree_centrality(DiG, output)
    output = out_degree_centrality(DiG, output)
    output = degree_centrality(DiG, output)
    output = in_degree(DiG, output)
    output = out_degree(DiG, output)
    output = degree(DiG, output)
    output = self_loops(DiG, output)
    df_nodes_self_loop_iteration = self_loop_iteration_nodes(df)
    output = merge_dataframes(output, df_nodes_self_loop_iteration)
    return output
    
def graph_json_values(df_graph, df_basic_data, node_list_df, from_verified):

    if (from_verified == False):            
        df_basic_data = df_basic_data[df_basic_data["verified"] != True].reset_index()

    node_list_verified_filter = list(df_basic_data["screen_name"])
    node_list_verified_filter_df= pd.DataFrame()
    node_list_verified_filter_df["nodes"]= node_list_verified_filter  

    #Removing incorrect profile mentions
    tweets_profiles =  list(df_basic_data["screen_name"])
    node_list = list(node_list_df["nodes"])
    
    delete_profiles = []            
    for item in node_list:
        if item not in tweets_profiles:
            delete_profiles.append(item)

    df_graph = df_graph[~df_graph["screen_name"].isin(delete_profiles)]
    df_graph = df_graph[~df_graph["screen_name_mention"].isin(delete_profiles)]    

    
    
    data = {}
    data['nodes'] = []
    for i in range(len(df_basic_data)):
      
      data['nodes'].append({
          'screen_name': df_basic_data["screen_name"].iloc[i],
          'community': str(df_basic_data["community"].iloc[i]),
          "community_degree_mean": float(df_basic_data["community_degree_mean"].iloc[i]),
          'followers': int(df_basic_data["followers"].iloc[i]),
          'following': int(df_basic_data["followees"].iloc[i]),
          'statuses_count': int(df_basic_data["statuses_count"].iloc[i]),
          'url': str(df_basic_data["url"].iloc[i])
      })
      
    data['edges'] = []
    for i in range(len(df_graph)):
        if(df_graph["screen_name_mention"].iloc[i] != "Empty"):        
            data['edges'].append({
              'screen_name': df_graph["screen_name"].iloc[i],
              'screen_name_mention': df_graph["screen_name_mention"].iloc[i],
              'iteration': str(df_graph["iteration"].iloc[i])
            })
      
    return data, node_list_verified_filter_df

def simple_user_timeline_extraction(node_list, consumerKey, consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups=1,save_by=300):
    # get_user Returns the 20 most recent statuses posted from the authenticating user or the user specified. 
    profile_iter = save_by
    k=0
    auth = tweepy.OAuthHandler(consumerKey[0], consumerSecret[0])
    auth.set_access_token(accessToken[0], accessTokenSecret[0])
    api = tweepy.API(auth)
    nc= 0
    ultima = 0
    origen1 = time.time()
    while ((k<= (len(node_list)+profile_iter)) & (ultima !=2) ):
      tweets_user=[]
      list_users_noInfo = []
      origen2 = time.time()
      i=0
      if ((len(node_list)>= k) & ((len(node_list)-profile_iter) <=k)):
        node_list1 = node_list[k:len(node_list)]
        ultima = 1
      else:
        node_list1 = node_list[k:k+profile_iter]
      while(i <(len(node_list1))):         
        pri = 0
        itera=0
        max_id=""
        intentos = 0
        while itera != n_groups:
          try:
            if pri ==0:
              user=api.user_timeline(node_list1[i], count=1,tweet_mode="extended")      
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              pri=1
              itera = itera+1
            else:
              user=api.user_timeline(node_list1[i], count=1,tweet_mode="extended", max_id=max_id)
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              itera = itera+1
              intentos=0 # Para si justo es el primero el que no se puede extraer y no es problema de agotar claves
          except:
            nc = nc+1
            n_clave = len(consumerKey)
            if(nc == n_clave):
              nc= 0
            auth = tweepy.OAuthHandler(consumerKey[nc], consumerSecret[nc])
            auth.set_access_token(accessToken[nc], accessTokenSecret[nc])
            api = tweepy.API(auth)
            intentos = intentos + 1
            if(intentos == 2):         
              list_users_noInfo.append(node_list1[i])
              intentos = 0
              itera=n_groups
        i = i+1       
      destino2 = time.time()
      aux=[]
      for i in range( len(tweets_user)):
        for j in range(len(tweets_user[i])):          
            aux.append(tweets_user[i][j]._json)     
      if(len(aux) != 0):  
        df = pd.DataFrame(aux)
        df = df.rename(columns = {"created_at": "created_at_tw"})
        df= df.rename(columns = {"lang": "lang_tw"})
        df = pd.concat([df.drop(['user'], axis=1), df['user'].apply(pd.Series)], axis=1)
        df2 = df.rename(columns={"followers_count": "followers",
                              "friends_count": "followees",
                              "retweet_count": "retweets",
                              "favorite_count": "favorites",
                              "favourites_count": "favorites_count",
                              "full_text": "text"})
        df2["url"] = "http://www.twitter.com/"+df2["screen_name"]
        if path.exists(os.path.join(filepath,filename+".csv")):
          df2.to_csv(path_or_buf =os.path.join(filepath,filename+".csv"),mode="a", index=False, header=False)
        else:
          df2.to_csv(path_or_buf = os.path.join(filepath,filename+".csv"),index=False)         
        if len(list_users_noInfo) !=0:
          nodes = pd.DataFrame()
          nodes["nodos"] = list_users_noInfo
          if path.exists(os.path.join(filepath,"node_without_",filename+".csv")):
            nodes.to_csv(path_or_buf = os.path.join(filepath,"node_without_"+filename+".csv"), mode ="a",index=False, header=False)          
          else:
             nodes.to_csv(path_or_buf = os.path.join(filepath,"node_without_"+filename+".csv"), index=False)
        k = k+profile_iter        
        if ultima ==1:          
          ultima =2
      else:
        print("Repetimos")
    print("Lista de usuarios sin metadata")
    print(list_users_noInfo)
    destino1 = time.time()
    return df2, list_users_noInfo




def user_timeline_extraction(node_list, consumerKey, consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups=1,save_by=300):
    # get_user Returns the 20 most recent statuses posted from the authenticating user or the user specified. 
    profile_iter = save_by
    k=0
    auth = tweepy.OAuthHandler(consumerKey[0], consumerSecret[0])
    auth.set_access_token(accessToken[0], accessTokenSecret[0])
    api = tweepy.API(auth)
    nc= 0
    ultima = 0
    origen1 = time.time()
    while ((k<= (len(node_list)+profile_iter)) & (ultima !=2) ):
      tweets_user=[]
      list_users_noInfo = []
      origen2 = time.time()
      i=0
      if ((len(node_list)>= k) & ((len(node_list)-profile_iter) <=k)):
        node_list1 = node_list[k:len(node_list)]
        ultima = 1
      else:
        node_list1 = node_list[k:k+profile_iter]
      while(i <(len(node_list1))):         
        pri = 0
        itera=0
        max_id=""
        intentos = 0
        while itera != n_groups:
          try:
            if pri ==0:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended")      
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              pri=1
              itera = itera+1
            else:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended", max_id=max_id)
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              itera = itera+1
              intentos=0 # Para si justo es el primero el que no se puede extraer y no es problema de agotar claves
          except:
            nc = nc+1
            n_clave = len(consumerKey)
            if(nc == n_clave):
              nc= 0
            auth = tweepy.OAuthHandler(consumerKey[nc], consumerSecret[nc])
            auth.set_access_token(accessToken[nc], accessTokenSecret[nc])
            api = tweepy.API(auth)
            intentos = intentos + 1
            if(intentos == 2):         
              list_users_noInfo.append(node_list1[i])
              intentos = 0
              itera=n_groups
        i = i+1       
      destino2 = time.time()
      aux=[]
      for i in range( len(tweets_user)):
        for j in range(len(tweets_user[i])):          
            aux.append(tweets_user[i][j]._json)     
      if(len(aux) != 0):  
        df = pd.DataFrame(aux)
        df = df.rename(columns = {"created_at": "created_at_tw"})
        df= df.rename(columns = {"lang": "lang_tw"})
        df = pd.concat([df.drop(['user'], axis=1), df['user'].apply(pd.Series)], axis=1)
        df = df.rename(columns={"followers_count": "followers",
                              "friends_count": "followees",
                              "retweet_count": "retweets",
                              "favorite_count": "favorites",
                              "favourites_count": "favorites_count",
                              "full_text": "text"})
        df2 = metadata_extraction(df)
        if path.exists(os.path.join(filepath,filename+".csv")):
          df2.to_csv(path_or_buf =os.path.join(filepath,filename+".csv"),mode="a", index=False, header=False)
        else:
          df2.to_csv(path_or_buf = os.path.join(filepath,filename+".csv"),index=False)         
        if len(list_users_noInfo) !=0:
          nodes = pd.DataFrame()
          nodes["nodos"] = list_users_noInfo
          if path.exists(os.path.join(filepath,"node_without_",filename+".csv")):
            nodes.to_csv(path_or_buf = os.path.join(filepath,"node_without_"+filename+".csv"), mode ="a",index=False, header=False)          
          else:
             nodes.to_csv(path_or_buf = os.path.join(filepath,"node_without_"+filename+".csv"), index=False)
        k = k+profile_iter        
        if ultima ==1:          
          ultima =2
      else:
        print("Repetimos")
    print("Lista de usuarios sin metadata")
    print(list_users_noInfo)
    destino1 = time.time()
    return df2, list_users_noInfo

def separate_text_tweets_feature(df_metadata):
  df_metadata["RT_days_list"] = 0
  df_metadata["lang_days_list"] = 0
  for k in range(len(df_metadata)):
    data_tweets = df_metadata.iloc[k]["text_tweets_days_list"]
    text_tweets_day = []
    text_tweets_days = []
    lang_text_tweets_day = []
    lang_text_tweets_days = []
    RT_text_tweets_day = []
    RT_text_tweets_days = []
    for i in range(len(data_tweets)):
      text_tweets_day = []
      lang_text_tweets_day = []
      RT_text_tweets_day = []
      if (len(data_tweets) ==1) & (len(data_tweets[0])==3):
        try:
          text_tweets_days.append(data_tweets[i]["text"]+"¿¿??##%")
          lang_text_tweets_days.append(data_tweets[i]["lang"])
          RT_text_tweets_days.append(str(data_tweets[i]["RT"]))
        except:
          for j in range(len(data_tweets[i])):
            text_tweets_day.append(data_tweets[i][j]["text"]+"¿¿??##%")
            lang_text_tweets_day.append(data_tweets[i][j]["lang"])
            RT_text_tweets_day.append(str(data_tweets[i][j]["RT"]))
          text_tweets_days.append(text_tweets_day)
          lang_text_tweets_days.append(lang_text_tweets_day)
          RT_text_tweets_days.append(RT_text_tweets_day) 
      else:
        for j in range(len(data_tweets[i])):
          text_tweets_day.append(data_tweets[i][j]["text"]+"¿¿??##%")
          lang_text_tweets_day.append(data_tweets[i][j]["lang"])
          RT_text_tweets_day.append(str(data_tweets[i][j]["RT"]))
        text_tweets_days.append(text_tweets_day)
        lang_text_tweets_days.append(lang_text_tweets_day)
        RT_text_tweets_days.append(RT_text_tweets_day)
    df_metadata["text_tweets_days_list"].iloc[k] = text_tweets_days    
    df_metadata["lang_days_list"].iloc[k] = lang_text_tweets_days
    df_metadata["RT_days_list"].iloc[k]= RT_text_tweets_days
  return df_metadata
  
#----------------------------------Extract metadata-----------------------------------------------------------#
def metadata_extraction (df_users):
    
	users = df_users["screen_name"].unique()
	count_users=0
	df = pd.DataFrame() 
	for i in range(len(users)):
		data_tweets = df_users[df_users["screen_name"]==users[i]].reset_index()
		
		data = pd.DataFrame()              
		if(data_tweets.empty == False):       
			count_users = count_users + 1
			print("Usuarios: %f" % count_users)
			[screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
			 fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_days_list,
			 text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,
			 tw_day_list] = text_tweets_features_extraction(data_tweets)
			data["screen_name_mention_user"] = screen_name_mention_user
			data["screen_name"] = data_tweets["screen_name"].iloc[0]  
			data["created_at"] = data_tweets["created_at"].iloc[0]
			data["following"] = data_tweets["followees"].iloc[0]
			data["followers"] = data_tweets["followers"].iloc[0]
			data["statuses_count"] = data_tweets["statuses_count"].iloc[0]
			data["default_profile"] = data_tweets["default_profile"].iloc[0]
			data["default_profile_image"] = data_tweets["default_profile_image"].iloc[0]
			data["biography_profile"] = data_tweets["description"].iloc[0]
			data["listed_count"] = data_tweets["listed_count"].iloc[0]    
			data["favourite_count"] = data_tweets["favorites_count"].iloc[0]
			data["seasonality"] = seasonalityDF    
			data["tweets_url"] = tweets_urlDF    
			data["mentions"] = mentionsDF 
			data["text_tweets_days_list"] = text_tweets_days_list
			data["tweet_date_days_list"] = tweet_date_days_list   
			data["text_tweets"] = text_tweetsDF
			data["favorite_tweets_list"] = fav_twDF_list
			data["retweet_tweets_list"] = ret_twDF_list
			data["favorite_tweets_count"] = fav_twDF
			data["retweet_tweets_count"] = ret_twDF
			data["RT"] = RT_tw
			data["num_ownTw"] = ntwPro_DF    
			data["time_btw_tw"] = minu_tw
			data["tw_day_list"] = tw_day_list
			data["tw_per_day_list"] = tw_per_days_list
			data["tw_duplicated"] = duplicated
			data["minu_tw_answer"] = minu_tw_answer
			data["profile_type"] = data_tweets["verified"].iloc[0]
			data["screen_name_mention_user"] = data["screen_name_mention_user"].astype(str)
			probably_fake = []
			for j in range(len(data)):
				if data["biography_profile"].any()==False:# Si se lee el dataframe
				#if len(data["biography_profile"][j]) == 0:# Si se hace la extraccion antes de guardar los datos
					data["biography_profile"][j] = 1
				else:
					data["biography_profile"][j] = 0
				if data["following"].iloc[j] == 2001:
					probably_fake.append(1)
				else:
					probably_fake.append(0)
			data["probably_fake"] = probably_fake
			df = df.append(data, ignore_index=True)
	df =df.loc[df.astype(str).drop_duplicates().index].reset_index()

	df = time_twitter_account(df)
	df = time_series_tw(df)
	df = separate_text_tweets_feature(df)
	return df



def text_tweets_features_extraction(data_tweets):
   
    seasonalityDF = []
    tweets_urlDF = []
    mentionsDF = []
    text_tweetsDF = []
    fav_twDF= []
    ret_twDF = []
    ret_twDF_list = []
    fav_twDF_list = []
    ntwPro_DF= []
    RT_tw = []
    minu_tw = []
    minu_tw_answer = []
    tw_duplicated = []
    duplicated = []
    tw_per_day_list= []
    screen_name_mention_user = []
    tweets = []
    tweets_url = 0
    num_tw_day = 1
    is_RT=0
    is_RT_list= []
    screen_name_mention = []
    RT = []
    retweet_list = []
    favorite_list = []
    mentions = 0
    time_btw_tw = []
    tw_answer = []
    num_tw_days = []
    text_duplicated = []
    tw_day_list = []
    text_tweets_day = []
    text_tweets_days = []
    text_tweets_days_list = []
    #Almacenar la fecha entera de los tweets para si hay que consultar las horas de ese dia
    tweet_date_day = []
    tweet_date_days = []
    tweet_date_days_list = []
    lang_text_tweet = list(data_tweets["lang_tw"])
    text_tweets_user= list(data_tweets["text"])
    favorites= list(data_tweets["favorites"])
    retweets = list(data_tweets["retweets"])
    tweets_date= pd.to_datetime(data_tweets["created_at_tw"])
    for j in range(len(text_tweets_user)): #Comprobamos cuantos tweets han sido escritos por el usuario 
      if (text_tweets_user[j].startswith('RT',0)):
        RT.append(text_tweets_user[j])
        is_RT = 1
      else:
        is_RT=0          
        #Tweets with url from users
        if "http" in text_tweets_user[j]:
          tweets_url = tweets_url + 1
        #Tweets with mentions from users
        if "@" in text_tweets_user[j]:
          mentions = mentions + 1                        
        else:
          #Time of the answer of a tweet(tw --> @)
          if(j!=(len(text_tweets_user)-1)):
            if ("@" in text_tweets_user[j+1]):
              tw_answer.append((tweets_date[j] - tweets_date[j+1]) / np.timedelta64(1,'m'))
          #Found duplicated tweets where the only change the photo  that the users publish
          text_sinHttp = " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split()))
          text_sinMencion = " ".join(filter(lambda x:x[0]!='@', text_sinHttp.split()))
          text_duplicated.append(text_sinMencion)
        tweets.append({"text":text_tweets_user[j], "lang": lang_text_tweet[j], "RT": 0})
        retweet_list.append(int(retweets[j]))
        favorite_list.append(int(favorites[j]))
      is_RT_list.append(is_RT)                                
      if (j!=0):
        #Time between tweets (RT + propios)
        time_btw_tw.append((tweets_date[j-1] - tweets_date[j]) / np.timedelta64(1,'m'))
        #Found if tweets are the same day
        #Second condition if all the tweets are the same day          
        if ((tweets_date[j-1].date() == tweets_date[j].date()) & (j!=(len(text_tweets_user)-1))):                        
          #Create a list with the tweets of a day
          text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
          #text_tweets_day.append({"text": text_tweets_user[j],"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
          tweet_date_day.append(tweets_date[j-1])
          #tweet_date_day.append(tweets_date[j])  
        else:
          if (j==(len(text_tweets_user)-1)):                  
            if (tweets_date[j-1].date() == tweets_date[j].date()):                     
              text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
              #text_tweets_day.append({"text": text_tweets_user[j],"lang": lang_text_tweet[j], "RT": is_RT_list[j]})           
              tweet_date_day.append(tweets_date[j-1])
              #tweet_date_day.append(tweets_date[j])
                                  
              text_tweets_days.append(text_tweets_day)
              tweet_date_days.append(tweet_date_day)
              num_tw_days.append(len(tweet_date_day))
              num_tw_day = 1 
              text_tweets_day = []
              tweet_date_day = []
            else:                      
              text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})				                                   
              tweet_date_day.append(tweets_date[j-1]) 
              num_tw_days.append(1)                     
              text_tweets_days.append(text_tweets_day)
              tweet_date_days.append(tweet_date_day)
              text_tweets_day = []
              tweet_date_day = []                      
              tweet_date_day.append(tweets_date[j])                     
              text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
              num_tw_days.append(1)
              text_tweets_days.append(text_tweets_day)
              tweet_date_days.append(tweet_date_day)
              num_tw_day = 1 
              text_tweets_day = []
              tweet_date_day = []                      
          else:
            if(num_tw_day ==1):
              text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})	
              tweet_date_day.append(tweets_date[j-1])                  
            text_tweets_days.append(text_tweets_day)
            tweet_date_days.append(tweet_date_day)
            num_tw_days.append(len(tweet_date_day))
            num_tw_day = 1 
            text_tweets_day = []
            tweet_date_day = []
      if "@" in (text_tweets_user[j]):
        split_text = text_tweets_user[j].split()
        check = "@"
        screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())] 
        if not screen_name_mention1:
          screen_name_mention.append(["Empty"])
        else:
          screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….,]", '',str(screen_name_mention1)).split(", ")
          if(text_tweets_user[j].startswith('RT',0)):
            screen_name_mention.append([screen_name_mention1[0]])                    
          else:
            screen_name_mention.append(screen_name_mention1)
      else:
        screen_name_mention.append(["Empty"])

    if(len(set(text_duplicated)) != len((text_duplicated))):
      duplicated.append(len(text_duplicated) - len(set(text_duplicated)))
    else:
      duplicated.append(0)
      
    #Maximun tweets for user
    if not num_tw_days:
      text_tweets_days_list.append([{"text":"Empty", "lang":"und","RT":2}])
      tweet_date_days_list.append(["Empty"])
      tw_per_day_list.append([0])
    else:
      text_tweets_days_list.append(text_tweets_days)
      tweet_date_days_list.append(tweet_date_days)
      tw_per_day_list.append(num_tw_days)

    tw_day_list.append(list(sorted(set(tweets_date.dt.date), reverse=True)))
    screen_name_mention_user.append(screen_name_mention)
    seasonalityDF.append(np.std(time_btw_tw))
    tweets_urlDF.append(tweets_url)
    mentionsDF.append(mentions)
    text_tweetsDF.append(tweets)
    fav_twDF_list.append(favorite_list)
    ret_twDF_list.append(retweet_list)
    fav_twDF.append(int(sum(favorite_list)))
    ret_twDF.append(int(sum(retweet_list)))
    ntwPro_DF.append(int(len(tweets)))
    RT_tw.append(int(len(RT)))
    minu_tw.append(int(sum(time_btw_tw)))
    #Time between tweets and its answer
    if not tw_answer:
      minu_tw_answer.append(0)
    else:   
      minu_tw_answer.append(int(sum(tw_answer))/len(tw_answer))
          
    return [screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
        fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_day_list,
        text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,tw_day_list]

def time_twitter_account(df):

    anio_actual = time.strftime("%Y")
    df["creation_day"] = 0
    df["twitter_years"] = 0
    for i in range(len(df)):
        df["creation_day"][i] = df.iloc[i]["created_at"].split(' ')[-1]
        df["twitter_years"][i] = int(anio_actual) - int(df['creation_day'][i]) + 1
    return df

def time_series_tw (df):
    for index, row in df.iterrows():
        restart=True
        while restart == True:
            restart=False
            for k in range(len(df.loc[index, "tw_day_list"])-1):
                if(int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days))>1:
                    times = int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days)
                    for j in range(times-1):
                        df.loc[index,"tw_per_day_list"].insert(k+1,0)
                        df.loc[index, "tweet_date_days_list"].insert(k+1,["Empty"])
                        df.loc[index,"text_tweets_days_list"].insert(k+1, [{"text":"Empty","lang": "und","RT":2}])
                        df.loc[index, "tw_day_list"].insert(k+j+1, (df.loc[index,"tw_day_list"][k] - timedelta(days=j+1)))
                    restart = True
    return df 


    #-------------------------------------------Ratios and other advanced features----------------------------------#
def duplicates_detection(data):
    
    data["possible_duplicates"] = 0
    data["close_duplicates"] = 0
    data["group_duplicates"] = 0
    close_duplicates_list =[]
    group_duplicates_list = []
    for i in range(len(data)):
        if i < len(data):
            possible_duplicated = []
            for j in range(len(data)):
                if j !=i:
                    list_dtw_1 = np.array(data["tw_per_day_list"].iloc[i])              
                    list_dtw_2 = np.array(data["tw_per_day_list"].iloc[j])
                    distance, path = fastdtw(list_dtw_1,list_dtw_2)
                    if (distance < 12600):
                        possible_duplicated.append({"screen_name":data["screen_name"].iloc[j], "distance": distance})
            close_duplicates= []
            group_duplicates = []
            if (len(possible_duplicated)!=0):              
                data["possible_duplicates"].iloc[i] = possible_duplicated                        
                for t in range(len(data["possible_duplicates"].iloc[i])):
                    #text_1 is the differences possible duplicates with the profile evaluate
                    text_1_aux = pd.DataFrame({"text":data[data["screen_name"] == data["possible_duplicates"].iloc[i][t]["screen_name"]]["text_tweets_days_list"]})
                    text_1 = pd.DataFrame()
                    for a in range(len(text_1_aux)):
                        aux2 = pd.DataFrame({'text':text_1_aux["text"].iloc[a]})
                        text_1 = text_1.append(aux2, ignore_index=False).reset_index(drop=True)
                    text_1_list = list(itertools.chain(*text_1["text"]))   
                    text_2_list = list(itertools.chain(*data.iloc[i]["text_tweets_days_list"]))               
                    if "Empty" in text_1_list:
                        text_1_list = list(filter(("Empty").__ne__, text_1_list))
                    if "Empty" in text_2_list:  
                        text_2_list = list(filter(("Empty").__ne__, text_2_list))
                    if "" in text_1_list:
                        text_1_list = list(filter(("").__ne__, text_1_list))
                    if "" in text_2_list:  
                        text_2_list = list(filter(("").__ne__, text_2_list))  
                    comparacion = [item for item in text_2_list if item in text_1_list]                         
                    if len(comparacion) > 0:
                        tw_similarity = len(comparacion)/(data["num_userTw"].iloc[i])
                        if (tw_similarity > 0.00003): 
                            group_duplicates.append(data["possible_duplicates"].iloc[i][t]["screen_name"])                           
                            close_duplicates.append({"screen_name":data["possible_duplicates"].iloc[i][t]["screen_name"], "distance": data["possible_duplicates"].iloc[i][t]["distance"],
                                                        "tw_similarity":tw_similarity, "tw_match_tw": comparacion})
                if len(close_duplicates) !=0:
                    group_duplicates.append(data["screen_name"].iloc[i])
                    group_duplicates_list.append(group_duplicates)
                    close_duplicates_list.append(close_duplicates)
                else:
                    group_duplicates_list.append("Empty")
                    close_duplicates_list.append("Empty")                    
            else:
                group_duplicates_list.append("Empty")
                close_duplicates_list.append("Empty")
    data["close_duplicates"] = close_duplicates_list
    data["group_duplicates"] = group_duplicates_list
    
    duplicate_profiles = data[data["group_duplicates"]!="Empty"].reset_index(drop=True)
    
    duplicate_profiles = hour_days_tweets(duplicate_profiles)
    group_of_duplicates_list=[]
    for i in range(len(duplicate_profiles)):
        group_of_duplicates_list.append(sorted(duplicate_profiles["group_duplicates"].iloc[i]))
    group_duplicates = list(group_of_duplicates_list for group_of_duplicates_list,_ in itertools.groupby(group_of_duplicates_list))
    data_group_duplicates = groups_duplicates_detection(group_duplicates,duplicate_profiles)
    return duplicate_profiles, data_group_duplicates

def groups_duplicates_detection(group_duplicates,data):
    data_final= {}
    for i in range(len(group_duplicates)):
        data_final["Group "+ str(i)]= []
        
        group_duplicate_tw_day_size = 0
        tw_day_list_size=[] 
        similar_tw_list = []
        for j in range(len(group_duplicates[i])):                    
            tw_day_list_size.append(len(data[data["screen_name"]==group_duplicates[i][j]]["tw_day_list"].iloc[0]))   
            #Create a list with all the tweets
            for v in range(len(data[data["screen_name"]==group_duplicates[i][j]]["close_duplicates"].iloc[0])):
                if (data.iloc[i]["close_duplicates"][v]["screen_name"]) in group_duplicates[i]:
                    similar_tw_list.append({"screen_name":data[data["screen_name"]==group_duplicates[i][j]]["close_duplicates"].iloc[0][v]["screen_name"],
                                            "text":(data[data["screen_name"]==group_duplicates[i][j]]["close_duplicates"].iloc[0][v]["tw_match_tw"])})
                    
        text_similar_tw_list = []
        if (len(similar_tw_list) !=0):
            #Aqui ya tenemos X listas con texto y fecha de los perfiles que hay en el grupo de duplicados. Ahora hay que ver si esos tweets estan en todos los perfiles
            find=False # Para ver si cada uno de los tweets del primer perfil esta en los demas
            for q in range(len(similar_tw_list[0]["text"])):
                for o in range(1,len(similar_tw_list)):
                    if (similar_tw_list[0]["text"][q] in similar_tw_list[o]["text"]):                  
                      find= True
                    else:
                      find = False
                date_list = []
                if (find==True): 
                    text_similar_tw_list.append(similar_tw_list[0]["text"][q])
            
            #Cada uno de los tweets de la lista tengo que buscarlos en el diccionario y crear la estructura dependiendo del numero de perfiles en el grupo para ya
            #finalizar el flujo
            data_similar_tweets_list = []
            for t in range(len(text_similar_tw_list)):
                date_similar_tw_profile = []
                for p in range(len(group_duplicates[i])):
                    group_profile_df = data[data["screen_name"]==group_duplicates[i][p]]     
                    date_profile = next(item for item in group_profile_df["text_date_dict"].iloc[0] if item["text"] == text_similar_tw_list[t])["date"].isoformat()
                    date_similar_tw_profile.append({"screen_name": group_profile_df["screen_name"].iloc[0], "date":date_profile})
                data_similar_tweets = {"tweet": text_similar_tw_list[t]}
                data_similar_tweets["publishInfo"] = date_similar_tw_profile
                data_similar_tweets_list.append(data_similar_tweets) 
        else:
          data_similar_tweets_list = []

        group_duplicate_tw_day_size =  min(tw_day_list_size)    
        group_info_list = []
        for j in range(group_duplicate_tw_day_size): 
            first={}
            first = {"date": data[data["screen_name"]==group_duplicates[i][0]]["tw_day_list"].iloc[0][j].isoformat()}
            for k in range(len(group_duplicates[i])):
                label_tw_profile= group_duplicates[i][k]
                first[label_tw_profile] = {"Número de tweets por dia": data[data["screen_name"]==group_duplicates[i][k]]["tw_per_day_list"].iloc[0][j],
                                        "Número de tweets por hora": data[data["screen_name"]==group_duplicates[i][k]]["tweets_hour_day_list"].iloc[0][j]}
            group_info_list.append(first)


        data_final["Group "+str(i)].append({
            "data": group_info_list,
            "group_duplicates": group_duplicates[i],
            "data_tweet_similar": data_similar_tweets_list
        })

    data_groups_duplicates = {}
    data_groups_duplicates["groups"] = data_final
    return data_groups_duplicates

def hour_days_tweets(df):
    df["tweets_hour_day_list"] = 0
    hour_days_tweets_list = []
    for j in range(len(df)):
        days = len(df.iloc[j]["tw_per_day_list"])
        data = df.iloc[j]    
        data["tweet_date_days_list_copy"] = copy.deepcopy(data["tweet_date_days_list"])
        hour_days_tweets = []
        for v in range(days):        
            date_list_day = data['tweet_date_days_list_copy'][v]
            if date_list_day !=["Empty"]:
                for t in range(len(date_list_day)):
                    date_list_day[t] = date_list_day[t].time().hour   
                x = list(range(0,24))
                y = []
                for k in range(len(x)):
                    count=0
                    for l in range(len(date_list_day)):        
                        if date_list_day[l] == k:
                            count = count + 1
                    y.append(count)
            else:
                y.append([0]*24)
            hour_days_tweets.append(y)
        hour_days_tweets_list.append(hour_days_tweets)
        
    df["tweets_hour_day_list"] = hour_days_tweets_list
    return df

def text_date_tweets_dict(data):
    data["text_date_dict"] = 0
    dict_profile_list= []
    for i in range(len(data)):
        dict_profile = []
        print(i)
        for j in range(len(data.iloc[i]["tweet_date_days_list"])):
            if (len(data.iloc[i]["tweet_date_days_list"])==1):
                for k in range(len(data.iloc[i]["text_tweets_days_list"][0])):
                    dict_profile.append({"text": data.iloc[i]["text_tweets_days_list"][0][k],
                                     "date": data.loc[i]["tweet_date_days_list"][0][k]})
            else:
                for k in range(len(data.iloc[i]["text_tweets_days_list"][j])):
                    dict_profile.append({"text": data.iloc[i]["text_tweets_days_list"][j][k],
                                     "date": data.loc[i]["tweet_date_days_list"][j][k]})
        dict_profile_list.append(dict_profile)
    data["text_date_dict"] = dict_profile_list
    return data 

	
def advanced_features(data):
    
    #Posible bot
    data["screen_name_bot"] = 0 
    data["days_with_tw"] = 0
    data["max_fav_tw"] = 0
    data["max_ret_tw"] = 0
    data["follow_rate"] = 0
    data["max_tw_day"] = 0
    data["index_max_day_tw"]=0
    data["possible_duplicates"] = 0
    data["fake_type"] = "Normal"

    data["num_userTw"]= data["num_ownTw"] + data["RT"]
    data["tw_RT_rate"] = ((((data["num_ownTw"]))) / (data["num_userTw"])).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["sum_fav_RT_ownTw"] = (data["retweet_tweets_count"] + data["favorite_tweets_count"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["iter_fav_RT_rate"] = (data["sum_fav_RT_ownTw"] / data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["tw_year_rate"] = ((data["statuses_count"]) / (data["twitter_years"])).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["time_tw_rate"] = (data["time_btw_tw"] / data["num_userTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["seasonality"] = data["seasonality"].replace([np.inf, -np.inf], np.nan).fillna(0)
    data["fake_sum"] = data["default_profile_image"] + data["biography_profile"]+ data["screen_name_bot"]
    data["fake_rate"] = ((data["tweets_url"] + data["mentions"]) /data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["follow_rate"][data["followers"]== 0] = np.median(data["follow_rate"])
    
    for i in range(len(data)):
        data["favorite_tweets_list"].iloc[i] = ast.literal_eval(data["favorite_tweets_list"].iloc[i])
        data["retweet_tweets_list"].iloc[i] = ast.literal_eval(data["retweet_tweets_list"].iloc[i])
        data["tw_per_day_list"].iloc[i] = ast.literal_eval(data["tw_per_day_list"].iloc[i])
        if (len(str(data.iloc[i]["screen_name"])) > 4):
            if((data.iloc[i]["screen_name"][-1].isdigit()) & (data.iloc[i]["screen_name"][-2].isdigit()) & 
                (data.iloc[i]["screen_name"][-3].isdigit()) &(data.iloc[i]["screen_name"][-4].isdigit())):
                data["screen_name_bot"].iloc[i] = 1
        else:
            data["screen_name_bot"].iloc[i] = 1   

        if(data.iloc[i]["following"]== 0):
            data["follow_rate"].iloc[i] = 0
        else:
            data["follow_rate"].iloc[i] = (data.iloc[i]["following"] / data.iloc[i]["followers"])
        
        #ast.literal_eval cuando se leen los datos del csv porque no recoge bien la lista de valores
        #Favorites and Retweets in their published tweets
        if not ((data["favorite_tweets_list"].iloc[i])):
            data["max_fav_tw"].iloc[i] = 0
        else:
            data["max_fav_tw"].iloc[i] = max((data["favorite_tweets_list"].iloc[i]))
        
        if not ((data["retweet_tweets_list"].iloc[i])):
            data["max_ret_tw"].iloc[i] = 0
        else:
            data["max_ret_tw"].iloc[i] = max((data["retweet_tweets_list"].iloc[i]))

        #Differentes types of fake
        data["default_profile_image"] + data["biography_profile"]+ data["screen_name_bot"]
        if ((data["default_profile_image"].iloc[i] == 0) & (data["biography_profile"].iloc[i] == 0) & (data["screen_name_bot"].iloc[i] == 0)):
            data["fake_type"].iloc[i] ="None"
        if ((data["default_profile_image"].iloc[i] == 1) & (data["biography_profile"].iloc[i] == 0) & (data["screen_name_bot"].iloc[i] == 0)):
            data["fake_type"].iloc[i] ="Default image"
        if ((data["default_profile_image"].iloc[i] == 0) & (data["biography_profile"].iloc[i] == 1) & (data["screen_name_bot"].iloc[i] == 0)):
            data["fake_type"].iloc[i] ="No biography"
        if ((data["default_profile_image"].iloc[i] == 0) & (data["biography_profile"].iloc[i] == 0) & (data["screen_name_bot"].iloc[i] == 1)):
            data["fake_type"].iloc[i] ="Last 4 numbers screen_name"
        if ((data["default_profile_image"].iloc[i] == 1) & (data["biography_profile"].iloc[i] == 1) & (data["screen_name_bot"].iloc[i] == 0)):
            data["fake_type"].iloc[i] ="Default image + No biography"
        if ((data["default_profile_image"].iloc[i] == 1) & (data["biography_profile"].iloc[i] == 0) & (data["screen_name_bot"].iloc[i] == 1)):
            data["fake_type"].iloc[i] ="Default image + Last 4 numbers screen_name"
        if ((data["default_profile_image"].iloc[i] == 0) & (data["biography_profile"].iloc[i] == 1) & (data["screen_name_bot"].iloc[i] == 1)):
            data["fake_type"].iloc[i] ="No biography + Last 4 numbers screen_name"
        if ((data["default_profile_image"].iloc[i] == 1) & (data["biography_profile"].iloc[i] == 1) & (data["screen_name_bot"].iloc[i] == 1)):
            data["fake_type"].iloc[i] ="All signs of fake account"

          
        data["max_tw_day"].iloc[i] =max((data["tw_per_day_list"].iloc[i]))
        data["days_with_tw"].iloc[i] = len(data["tw_per_day_list"].iloc[i])
        data["index_max_day_tw"].iloc[i] = data["tw_per_day_list"].iloc[i].index(data["max_tw_day"].iloc[i])        
    data = trend_tweets_features(data) 
        
    return data
	
def trend_tweets_features(data):
    data["num_anom"] = 0
    data["trend"] = 0
    data["anom_rate"] = 0
    for i in range(len(data)):
        #trend rates
        if len(data.iloc[i]["tw_per_day_list"]) >4:
			#Select 95% confidence interval of a normal distribution to say that a values of tweet per day is an outlier
            df_aux= pd.DataFrame(data.iloc[i]["tw_per_day_list"])
            df_aux["floor"] = df_aux[0].mean() - 1.64 * df_aux[0].std()
            df_aux["roof"] = df_aux[0].mean() + 1.64 * df_aux[0].std() 
			#
            df_aux["anom"] = df_aux.apply(lambda row: row[0] if (row[0]<= row["floor"] or 
                                                                 row[0]>= row["roof"]) else 0, axis =1) 
            data["num_anom"].iloc[i] = len(list(filter(lambda x: x != 0, df_aux["anom"])))
            data["anom_rate"].iloc[i] = data["num_anom"].iloc[i] / len(data["tw_per_day_list"].iloc[i])
            if (data["num_anom"].iloc[i] ==1):
                if max(df_aux["anom"])== data["max_tw_day"].iloc[i]:
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1                    
            else:
                if data["max_tw_day"].iloc[i] in list(filter(lambda x: x != 0, df_aux["anom"])):                    
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1  
        else:
            data["trend"].iloc[i] =2 
            data["num_anom"].iloc[i] =0
            data["anom_rate"].iloc[i]=0
    return data


	
def text_to_list_features_conversor (data):
    for index, row in data.iterrows():
        #data["favorite_tweets_list"].iloc[index] = ast.literal_eval(data.loc[index, "favorite_tweets_list"])
        #data["retweet_tweets_list"].iloc[index] = ast.literal_eval(data.loc[index,"retweet_tweets_list"])
        #data["tw_per_day_list"].iloc[index] = ast.literal_eval(data.loc[index,"tw_per_day_list"])
        data["text_tweets_days_list"].iloc[index] = data.loc[index,"text_tweets_days_list"].replace('"', "'").replace("], [","?#??").strip("[]'").split("?#??")
        list_day = []                                                                                
        list_text_tweets_day = []
        list_tweet_date_days = []
        list_RT_days = []
        list_lang_days = []
        text_days = data.loc[index,"tw_day_list"].strip("][").replace(")", ")??").split("??, ")
        tweet_date_days = data.loc[index,"tweet_date_days_list"].replace("], [","???").split("???")
        RT_days = data.loc[index, "RT_days_list"].strip("[]").split("], [")
        lang_days = data.loc[index, "lang_days_list"].strip("[]").split("], [")
        for i in range(len(text_days)):
            tweet_date_day = tweet_date_days[i].replace("), ",")??").strip("[]").split("??")
            text_tweets_day = data["text_tweets_days_list"].iloc[index][i].replace('"', "'").replace("¿¿??##%', '","¿¿??##%").strip("[]'").split("¿¿??##%")[:-1]
            RT_day = list(ast.literal_eval(str(RT_days[i])))
            if len(lang_days[i])<6:
                lang_day = [lang_days[i]]
            else:
                lang_day = list(ast.literal_eval(lang_days[i]))
            list_tweet_date_day = []
            for j in range(len(tweet_date_day)):                
                if(tweet_date_day == ["'Empty'"]):
                    list_tweet_date_day.append("Empty")
                else:
                    list_tweet_date_day.append(datetime.strptime(tweet_date_day[j],"Timestamp('%Y-%m-%d %H:%M:%S%z', tz='UTC')"))    
            if i == len(text_days)-1:
                text_days[i] = text_days[i].replace("??","")
            list_day.append(datetime.strptime(text_days[i],'datetime.date(%Y, %m, %d)' ).date())
            list_text_tweets_day.append(text_tweets_day)
            list_tweet_date_days.append(list_tweet_date_day)
            list_RT_days.append(RT_day)
            list_lang_days.append(lang_day)
        data["text_tweets_days_list"].iloc[index] = list_text_tweets_day
        data["tw_day_list"].iloc[index]= list_day
        data["tweet_date_days_list"].iloc[index]= list_tweet_date_days
        data["RT_days_list"].iloc[index] = list_RT_days
        data["lang_days_list"].iloc[index] = list_lang_days
    return data
	

#----------------------------------------------Filters-------------------------------------------------------#
def abnormal_categories_profiles(data_join):

    
    data_join["evaluate_NLP"] = "0"
    for i in range(len(data_join)):
        abnormal_category_belonging = []
        #1.Profiles old spreader
        if ((data_join["index_max_day_tw"].iloc[i] >=30) & (data_join["profile_type"].iloc[i]==False) &
                      (data_join["max_tw_day"].iloc[i]>60)):
            abnormal_category_belonging.append("Old Spreader")  
        
        #2.Profiles with low number of tweets but with a high iteration
        if((data_join["trend"].iloc[i] == 0) & (data_join["profile_type"].iloc[i]==False) &
                      (data_join["max_tw_day"].iloc[i]<40) & (data_join["tw_RT_rate"].iloc[i]<0.2) &
                     ((data_join["max_ret_tw"].iloc[i]>500) | (data_join["max_fav_tw"].iloc[i]>500))):
            abnormal_category_belonging.append("LRT_HI")
            
        #3.Profiles with a high number of RT in a specific day (try to spread information)
        if((data_join["trend"].iloc[i] == 0) & (data_join["profile_type"].iloc[i]==False) &
                      (data_join["max_tw_day"].iloc[i]>150) & (data_join["tw_RT_rate"].iloc[i]<0.1)):
            abnormal_category_belonging.append("HRT_SD")
            
        #4.Possible influencer profile
        if((data_join["trend"].iloc[i]==1) & (data_join["profile_type"].iloc[i]==False) &
                 (data_join["in_degree"].iloc[i]>=5) & (data_join["followers"].iloc[i]>=3000)):
            abnormal_category_belonging.append("Influencer")
        
        #5.Possible constant spreader
        if((data_join["trend"].iloc[i]==1) & (data_join["profile_type"].iloc[i]==False) &
                 (data_join["out_degree"].iloc[i]>=2) & (data_join["following"].iloc[i]>=3000)):
            abnormal_category_belonging.append("Constant Spreader")                

        #6.Possible new account with a high activity last days
        if((data_join["trend"].iloc[i]==2) & (data_join["profile_type"].iloc[i]==False) &
                 (data_join["twitter_years"].iloc[i]==1) & (data_join["max_tw_day"].iloc[i]>210)):
            abnormal_category_belonging.append("NP_HA")                     

        #7.Possible fake behaviour profile in the last days
        if((data_join["trend"].iloc[i]==2) & (data_join["profile_type"].iloc[i]==False) &
                 (data_join["fake_sum"].iloc[i]>=2)):
            abnormal_category_belonging.append("Fake Behaviour") 
        
        #8.Possible influencers profile in the last days with a high iteration
        if((data_join["trend"].iloc[i]==2) & (data_join["profile_type"].iloc[i]==False) &
                 ((data_join["max_ret_tw"].iloc[i]>500) | (data_join["max_fav_tw"].iloc[i]>500)) &
                      (data_join["max_tw_day"].iloc[i]>210)):
            abnormal_category_belonging.append("Influ_LD_HI")
        
        #9.Profiles BOT (more than tweet or RT each 5 minutes the 24 hours)
        if((data_join["max_tw_day"].iloc[i]>288) &(data_join["profile_type"].iloc[i]==False)):
            abnormal_category_belonging.append("BOT")
                                 
        #10. More data required
        if((data_join["trend"].iloc[i]==2) & (data_join["profile_type"].iloc[i]==False) & 
                                  (data_join["max_tw_day"].iloc[i]>180)):
            abnormal_category_belonging.append("More Data")
        
        if len(abnormal_category_belonging)!=0:
            data_join["evaluate_NLP"].iloc[i] = abnormal_category_belonging     
        else:
            abnormal_category_belonging.append("No")
            data_join["evaluate_NLP"].iloc[i] = abnormal_category_belonging     
        
    return data_join

	
def more_tweets_required2(df,df_graph_features,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath,filename,n_groups,save_by):
	df_evaluate = df[(df["evaluate_NLP"] !="No") & (df["evaluate_NLP"] !="More Data")]
	node_list_moreData = list(df[df["evaluate_NLP"]=="More Data"]["screen_name"])
	if len(node_list_moreData) >0:
		df_metadata_moreData, list_more_Data_noData = user_timeline_extraction(node_list_moreData,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups,save_by)
		df_metadata_moreData = pd.read_csv(filepath + filename)
		df_metadata_moreData = text_to_list_features_conversor(df_metadata_moreData)
		df_metadata_moreData = advanced_features(df_metadata_moreData)
		df_metadata_moreData = merge_dataframes(df_metadata_moreData,df_graph_features)
		df_metadata_moreData = abnormal_categories_profiles(df_metadata_moreData)
		df_metadata_moreData = df_metadata_moreData[(df_metadata_moreData["evaluate_NLP"] !="No") & (df_metadata_moreData["evaluate_NLP"] !="More Data")]
		df_evaluate = df_evaluate.append(df_metadata_moreData, ignore_index=True)
	return df_evaluate
	
def more_tweets_required(df,df_graph_features,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath,filename,n_groups,save_by):
    df_evaluate = df.copy()
    node_list_moreData = []
    delete_rows = []
    for i in range(len(df)):
        if "More Data" in df["evaluate_NLP"].iloc[i]:
            node_list_moreData.append(df["screen_name"].iloc[i]) 
            delete_rows.append(i)           
        if "No" in df["evaluate_NLP"].iloc[i]:
            delete_rows.append(i)
    df_evaluate= df_evaluate.drop(df_evaluate.index[delete_rows]).reset_index(drop=True)
    if len(node_list_moreData) >0:
        df_metadata_moreData, list_more_Data_noData = user_timeline_extraction(node_list_moreData,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups,save_by)
        df_metadata_moreData = pd.read_csv(os.path.join(filepath,filename+".csv"))
        #df_metadata_moreData = text_to_list_features_conversor(df_metadata_moreData)
        df_metadata_moreData = advanced_features(df_metadata_moreData)
        df_metadata_moreData = merge_dataframes(df_metadata_moreData,df_graph_features)
        df_metadata_moreData = abnormal_categories_profiles(df_metadata_moreData)
        delete_rows = []
        for i in range(len(df_metadata_moreData)):
          if (("More Data" in df_metadata_moreData["evaluate_NLP"].iloc[i]) | ("No" in df_metadata_moreData["evaluate_NLP"].iloc[i])): 
              delete_rows.append(i)
        df_metadata_moreData= df_metadata_moreData.drop(df.index[delete_rows])
        df_metadata_moreData= df_metadata_moreData.reset_index(drop=True)
        df_evaluate = df_evaluate.append(df_metadata_moreData, ignore_index=True)
    return df_evaluate

def contextual_analysis_profile(data, keyword_corpus, hashtag_corpus):
    n_list_tw = range(0, len(data["tw_per_day_list"]))
    #To remember which name of the tw_per_day_list belongs each tweets
    aux = pd.DataFrame({'text':data["text_tweets_days_list"],'RT':data["RT_days_list"],'lang': data["lang_days_list"], 'n_list_tw':n_list_tw})
    tweets_df = pd.DataFrame()
    for i in range(len(aux)):
      aux2 = pd.DataFrame({'text':aux["text"].iloc[i],'RT':aux["RT"].iloc[i],'lang': aux["lang"].iloc[i],"n_list_tw": aux["n_list_tw"].iloc[i]})
      tweets_df = tweets_df.append(aux2, ignore_index=False).reset_index(drop=True)
    tweets_df = tweets_df[tweets_df["RT"] !="2"].reset_index(drop=True)
    tweets_df = sentimental_analysis_features(tweets_df)
    sample_data_tokenized = tokenize_tweets(tweets_df)
    tweets_df = keyword_score(tweets_df, sample_data_tokenized,keyword_corpus)
    tweets_df = hashtag_score(tweets_df,hashtag_corpus)	
    tweets_df["terrorist_suggestion"] = 0
    tweets_df["terrorist_suggestion"][(tweets_df["hashtag_score"]>0) | (tweets_df["keyword_score"]>0)] = 1
    tweets_irr_words = len(tweets_df[tweets_df["terrorist_suggestion"]==1])
    if len(tweets_df[tweets_df["terrorist_suggestion"]==1]) == 0:
      data["per_hash_key"] = 0
      data["negative_opinion"] = 0
      data["negative_fact"] = 0
      data["neutral"] = 0
      data["positive_fact"] = 0
      data["positive_opinion"] = 0
    else:
      data["per_hash_key"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==1]) / len(tweets_df))
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] <= -0.1) & (tweets_df["subjectivity"]>=0.6)]= 2 #negative opinion
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] <= -0.1) & (tweets_df["subjectivity"]<0.6)]= 3 # negative fact
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] < 0.1) & (tweets_df["polarity"] > -0.1)]= 4 #neutral
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] >= 0.1) & (tweets_df["subjectivity"]<=0.5)]= 5 #positive fact
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] >= 0.1) & (tweets_df["subjectivity"]>0.5)]= 6 #positive opinion
      if len(tweets_df[tweets_df["terrorist_suggestion"]==2]) == 0:
        data["negative_opinion"] = 0
      else:
        data["negative_opinion"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==2]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==3]) == 0:
        data["negative_fact"] = 0
      else:
        data["negative_fact"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==3]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==4]) == 0:
        data["neutral"] = 0
      else:
        data["neutral"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==4]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==5]) == 0:
        data["positive_fact"] = 0
      else:
        data["positive_fact"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==5]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==6]) == 0:
        data["positive_opinion"] = 0
      else:
        data["positive_opinion"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==6]) / tweets_irr_words)
      
      tw_per_day_list_terrtw=[]
      for i in range(len(data["tw_per_day_list"])):
        tw_per_day_list_terrtw.append(len((tweets_df[(tweets_df["terrorist_suggestion"] !=0) & (tweets_df["n_list_tw"]==i)])))
      data["tw_per_day_list_terrTw"] = tw_per_day_list_terrtw
    return data,tweets_df

	
def contextual_analysis_profiles(data,keyword_corpus, hashtag_corpus):	
	final_df= pd.DataFrame()
	for i in range(len(data)):
		profile_evaluated, tweets_df = contextual_analysis_profile(data.iloc[i], keyword_corpus, hashtag_corpus)
		final_df = final_df.append(profile_evaluated, ignore_index=True)
	return final_df
	
def profile_trend_visualization(data, index):
	time_likes = pd.Series(data=data, index=index)
	time_likes.plot(figsize=(20, 8), color='r')
	plt.title('Daily Trend of Tweets',fontsize=20)
	plt.xlabel('Date',fontsize=15)
	plt.ylabel('Number of tweets',fontsize=15)
	plt.show()

def profile_max_tw_day_hourly_visualization(data):
	data["tweet_date_days_list_copy"] = copy.deepcopy(data["tweet_date_days_list"])
	date_list =data['tweet_date_days_list_copy'][data["index_max_day_tw"]]
	for i in range(len(date_list)):
		date_list[i] = date_list[i].time().hour    
	x = list(range(0,24))
	y = []
	for i in range(len(x)):
		count=0
		for j in range(len(date_list)):        
			if date_list[j] == i:
				count = count + 1
		y.append(count)
	del data["tweet_date_days_list_copy"]
	plt.title('Hourly Trend of Tweets around Max. Tweets',fontsize=20)
	plt.xlabel('Hour of the day',fontsize=15)
	plt.ylabel('Number of tweets',fontsize=15)
	plt.axis([0,23,0, max(y)+5])
	plt.locator_params(axis='x', nbins=24)
	plt.rcParams['figure.figsize'] = [10, 8]
	plt.plot(x,y)

	
def sentimental_analysis_features(data):
	corpus =[]
	polarities=[]
	subjectivities=[]
	for tweet in data.text:
		corpus.append(TextBlob(tweet.lower()))
	for i in range(len(corpus)):
		polarities.append(corpus[i].polarity)
		subjectivities.append(corpus[i].subjectivity)
	data['polarity']= polarities
	data['subjectivity']= subjectivities
	return data

def distribution_sentiment_tweets(data):
	### VISUALIZATION
	plt.rcParams['figure.figsize'] = [40, 20]
	for i in range (len(data)):
		x=data.polarity.iloc[i]
		y=data.subjectivity.iloc[i]
		if x>0.1 : # blue   red
			if y>0.5:  # yellow   green
				plt.scatter(x,y, color='blue')
			else: 
				plt.scatter(x,y, color='pink')
		elif -0.1<=x<=0.1:
			plt.scatter(x,y, color='gold')
		else:
			if y>0.5:  # yellow   green
				plt.scatter(x,y, color='purple')
			else: 
				plt.scatter(x,y, color='red')  
	plt.text(x+0.01, y+0.01, 'tweet'+str(i), fontsize=10)
	plt.xlim(-1,1)
	plt.ylim(0,1)
	plt.title('Scatter plot of sentiment analysis',fontsize=20)
	plt.xlabel('<------------------ NEGATIVE ------------------   POLARITY ------------------ POSITIVE ------------------>',fontsize=15)
	plt.ylabel('<----------------- FACTS ------------------ SUBJECTIVITY ------------------ OPINIONS ----------------->',fontsize=15)
	plt.show()

def general_pieChart(data):
	plt.rcParams['figure.figsize'] = [9, 6]	
	p=0 # positive
	n=0 # Negative
	o=0 # neutral
	for i in range(len(data)):
		if data['polarity'].iloc[i]>0.1:
			p+=1
		elif data['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	kn=0
	for i in range(len(data)):
	  if data['subjectivity'].iloc[i]>0.5:
		  op+=1
	  else:
		  f+=1
	plt.rcParams['figure.figsize'] = [10,5]
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['blue','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice

	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['pink','red']
	explode2=(0,0)

	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('The General Sentiment Analysis of all The tweets')
	plt.axis('equal')
	plt.show()
	

	
def tokenize_tweets(data):
	sample_data_tokenized=[]  
	tokenizer=RegexpTokenizer(r'\w+')
	for tweets in data.text:
		sample_data_tokenized.append(tokenizer.tokenize(tweets.lower()))
	return sample_data_tokenized
	
def define_hashtags(data):
	hashtags=[]
	for i in range(len(data)):
		h= (re.findall(r"#(\w+)", data.text.iloc[i]))
		t=[]
		for i in range(len(h)):
			t.append('#'+h[i].lower())
		hashtags.append(t)
	data['hashtags']=hashtags
	return data

def hashtag_score(data, hashtags_corpus):
    scores=[]
    hashtags = []
    data = define_hashtags(data)
    for hshtgs in data.hashtags:
      score = 0
      hashtag = []
      for h in hshtgs:
        #print(h)
        for H in hashtags_corpus.hashtags:
          if h == H:
            score += 1
            hashtag.append(h)
      hashtags.append(hashtag)      
      scores.append(score)
    data['hashtag_score'] = scores
    data["terrorist_hashtags"] = hashtags
    data['index'] = [i for i in range(len(data))]
    data['names']= ['TWEET '+str(i) for i in range(len(data))]
    return data
	
def keyword_score(data,sample_data_tokenized, keyword_corpus):
    scores = []
    words_list= []
    for i in range(len(sample_data_tokenized)):
      score=0
      words = []
      for c in keyword_corpus.keywords:
        for t in sample_data_tokenized[i]:         
          if c==t:
            words.append(c)
            score+=1
      try:
        scores.append(score/len(sample_data_tokenized[i]))
        words_list.append(words)
      except ZeroDivisionError:
        scores.append(0)
        words_list.append(0)
    data["keyword_match"] = words_list
    data['keyword_score']=scores
    return data


def terrorist_keywords_belonging(data):
	temp = data[data['keyword_score']>0].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(36,8), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.keyword_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.keyword_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Terrorist Corpus Belonging Score of the Tweets', fontdict={'size':22})
	ax.set_ylabel('Belonging Score of each tweet to the cluster' )
	ax.set_ylabel('Tweets')
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 1)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index, row.keyword_score+0.15,rotation=90, s=round(row.keyword_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()
	
def pie_chart_keywords_terrorist(data):
	plt.rcParams['figure.figsize'] = [9, 6]
	data_terr = data[data['keyword_score']>0.2].reset_index(drop=True)
	p=0
	n=0
	o=0
	for i in range(len(data_terr)):
		if data_terr['polarity'].iloc[i]>0.1:
			p+=1
		elif data_terr['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(data_terr)):
		if data_terr['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('From '+str(len(data))+' tweets, '+ str(len(data_terr))+' are having Terrorist Corpus Score ')
	plt.axis('equal')
	plt.show()
	

def terrorist_hashtags_belonging(data):
	temp = data[ data['hashtag_score']>0].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(24,8), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.hashtag_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.hashtag_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Terrorist Hashtags Network Belonging Score of the Tweets', fontdict={'size':22})
	ax.set_ylabel('Number of Terrorist Hashtags' )
	ax.set_ylabel('Tweets')
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 10)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index+0.01, row.hashtag_score+0.15,rotation=90, s=round(row.hashtag_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()

def pie_chart_hashtags_terrorist(data):
	plt.rcParams['figure.figsize'] = [9, 6]
	temp = data[data['hashtag_score']>0].reset_index(drop=True)  
	p=0
	n=0
	o=0
	for i in range(len(temp)):
		if temp['polarity'].iloc[i]>0.1:
			p+=1
		elif temp['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(temp)):
		if temp['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1

	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('From '+str(len(data))+' tweets, '+ str(len(temp))+' tweets are following Terroristic Hashtags')
	plt.axis('equal')
	plt.show() 

def terrorist_tweets_classification_pieChart(data):

    plt.rcParams['figure.figsize'] = [9, 6]

    po = data["positive_opinion"]
    pf = data["positive_fact"]
    neu = data["neutral"]
    nf = data["negative_fact"]
    no = data["negative_opinion"]
    labels = 'Positive opinion', 'Positive fact','Neutral','Negative fact','Negative opinion'
    sizes = [po,pf,neu,nf,no]
    colors = ['blue','red', 'gold','yellowgreen', 'lightcoral']
    explode = (0,0,0,0,0)  # explode 1st slice

    fig, (ax1) = plt.subplots(1, 1)
    # Plot
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Sentiment of the tweets with terrostic contents')
    plt.axis('equal')
    plt.show()	
	
def distribution_sentiment_terrorist_tweets(tweets_df):
    ### VISUALIZATION
    plt.rcParams['figure.figsize'] = [20, 12]
    for i in range (len(tweets_df)):
      if tweets_df["terrorist_suggestion"].iloc[i] != 0:
        x=tweets_df.polarity.iloc[i]
        y=tweets_df.subjectivity.iloc[i]
        if x>0.1 : # blue   red
          if y>0.5:  # yellow   green
            plt.scatter(x,y, color='blue')
          else: 
            plt.scatter(x,y, color='pink')
        elif -0.1<=x<=0.1:
          plt.scatter(x,y, color='gold')
        else:
          if y>0.5:  # yellow   green
            plt.scatter(x,y, color='purple')
          else: 
            plt.scatter(x,y, color='red')  
    plt.xlim(-1,1)
    plt.ylim(0,1)
    plt.title('Scatter plot of sentiment analysis for terrorist contents',fontsize=20)
    plt.xlabel('<------------------ NEGATIVE ------------------   POLARITY ------------------ POSITIVE ------------------>',fontsize=15)
    plt.ylabel('<----------------- FACTS ------------------ SUBJECTIVITY ------------------ OPINIONS ----------------->',fontsize=15)
    plt.show()

  
 ###---------------------------------------------Telegram Functions -----------------------------------###

def load_telegram_file(json_filename):
    data = json.load(json_filename)
    df = pd.DataFrame(data)
    return df

def nodes_participants_dict(participants_df):
    l=[]
    for i in range(len(participants_df)):
        if str(participants_df.last_name.iloc[i]) != 'None':
            name = str(participants_df.first_name.iloc[i]) +' '+ str(participants_df.last_name.iloc[i])
        else:
            name = participants_df.first_name.iloc[i]
        l.append((participants_df._id.iloc[i], name))

    nodes_participants_dict= dict(l)
    return nodes_participants_dict


def nodes_participants_df(participants_df):
    l=[]
    for i in range(len(participants_df)):
        if str(participants_df.last_name.iloc[i]) != 'None':
            name = str(participants_df.first_name.iloc[i]) +' '+ str(participants_df.last_name.iloc[i])
        else:
            name = participants_df.first_name.iloc[i]
        l.append((participants_df._id.iloc[i], name))
    nodes_participants_df = pd.DataFrame(data=l , columns=['_id','name'])
    return nodes_participants_df



def messages_connections (msg, node_participants_dict):

    #Añade una variable en un otra variable diccionario
    l=[]
    for i in range(len(msg)):
        l.append(msg.from_id.iloc[i]['user_id'])
    msg['sender_id'] = l
    source = []
    target = []
    for i in range(len(msg)):
        if msg.reply_to.iloc[i] != None :
            replyid = msg.reply_to.iloc[i]['reply_to_msg_id']       
            source.append( msg.sender_id.iloc[i])
            target.append(int(msg[msg['_id']==replyid].sender_id))
    graph_rel = pd.DataFrame()
    graph_rel ['screen_name'] = source
    graph_rel ['screen_name_mention'] = target

    s=[]
    for i in range(len(graph_rel)):        
        try:
            s.append([node_participants_dict[graph_rel.screen_name.iloc[i]],node_participants_dict[graph_rel.screen_name_mention.iloc[i]]])
        except KeyError:
             print(graph_rel.screen_name_mention.iloc[i], 'this ID has left the group!')
    df_graph_connections = pd.DataFrame(data=s,columns = ['screen_name','screen_name_mention'])
    df_graph_connections ['iteration'] = [1 for i in range(len(df_graph_connections))]
    return df_graph_connections


def df_graph_telegram_features (DiG, nodes_participants_df):
    DiG.remove_nodes_from(['_id','name'])
    DiG.add_nodes_from(nodes_participants_df['name'])
    nodes_names= list(DiG.nodes())
    neighbours_names=[]
    in_deg = []
    out_deg = []
    degree_cent =[]
    closeness_cent = []
    betweenness_centrality = []
    load_centrality =[]
    eigenvector_centrality =[]
    for i in range(len(nodes_names)):
        neighbours_names.append(list(nx.all_neighbors(DiG, node=nodes_names[i])))
        in_deg.append(DiG.in_degree()[str(nodes_names[i])])
        out_deg.append(DiG.out_degree()[str(nodes_names[i])])
        degree_cent.append(nx.degree_centrality(DiG)[str(nodes_names[i])])
        closeness_cent.append(nx.closeness_centrality(DiG)[str(nodes_names[i])])
        betweenness_centrality.append(nx.betweenness_centrality(DiG)[str(nodes_names[i])])
        load_centrality.append(nx.load_centrality(DiG)[str(nodes_names[i])])
        eigenvector_centrality.append(nx.eigenvector_centrality(DiG)[str(nodes_names[i])])
    df_graph_features = pd.DataFrame()
    df_graph_features['screen_name']=nodes_names
    df_graph_features['in_degree'] = in_deg
    df_graph_features['out_degree'] = out_deg
    df_graph_features['degree'] = df_graph_features['in_degree']  + df_graph_features['out_degree']
    df_graph_features['degree_centrality'] = degree_cent
    df_graph_features['closeness_centrality'] = closeness_cent
    df_graph_features['betweenness_centrality'] = betweenness_centrality
    df_graph_features['load_centrality'] = load_centrality
    df_graph_features['eigenvector_centrality'] =eigenvector_centrality
    df_graph_features["neighbours"] = neighbours_names
    return df_graph_features

def graph_json_values_telegram(df_connections, data_graph_structure):

    data = {}
    data['nodes'] = []
    for i in range(len(data_graph_structure)):
      
      data['nodes'].append({
          'screen_name': data_graph_structure["screen_name"].iloc[i],
          'community': str(data_graph_structure["community"].iloc[i]),
          "community_degree_mean": float(data_graph_structure["community_degree_mean"].iloc[i])
      })
      
    data['edges'] = []
    for i in range(len(df_connections)):
        if(df_connections["screen_name_mention"].iloc[i] != "Empty"):        
            data['edges'].append({
              'screen_name': df_connections["screen_name"].iloc[i],
              'screen_name_mention': df_connections["screen_name_mention"].iloc[i],
              'iteration': str(df_connections["iteration"].iloc[i])
            })
      
    return data

###----------------------Contextual Analysis Telegram -----------------------###

def messages_preprocessing(msg, nodes_participants_dict):
    l=[]
    for i in range(len(msg)):
        l.append(msg.from_id.iloc[i]['user_id'])
    msg['sender_id'] = l
    msg["screen_name"] = ""
    for i in range(len(msg)):
        try:
            msg["screen_name"].iloc[i] = nodes_participants_dict[msg["sender_id"].iloc[i]]
        except:
            msg["screen_name"].iloc[i] = "This ID Left the group"
    return msg

def detectLanguge(msg):
    lan=[]
    for i in range(len(msg)):
        x=( re.sub("[^a-zA-Z]", " ",str(msg.message.iloc[i])))
        x=re.sub(' +', ' ', x)
        if x == 'None':
            lan.append('Not defined')
        elif x == '':
            lan.append('Not defined')
        elif x == ' ':
            lan.append('Not defined')
        else:
            lan.append(detect(x)) 
    
    msg['language'] = lan    
    return msg

def translateToEnglish(msg):
    translator = Translator()
    l=[]
    for i in range(len(msg)):
        if msg.language.iloc[i] == 'en':
            l.append(msg.message.iloc[i])
        elif msg.message.iloc[i] == None or msg.message.iloc[i] == '':
            l.append('')
        else:
            translation = translator.translate( msg.message.iloc[i], dest='en')
            l.append(translation.text)
    msg['translated_message'] = l
    return msg 

def cosine_distance_countvectorizer_method(s1, s2):
    
    # sentences to list
    allsentences = [s1 , s2]
    
    # packages
    from sklearn.feature_extraction.text import CountVectorizer
    from scipy.spatial import distance
    
    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()
    
    # distance of sifomilarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    cosine_similarity = round((1-cosine),4)
    #print('Similarity of two sentences are equal to ',round((1-cosine)*100,2),'%')
    return cosine_similarity

def content_similitarity(msg, corpus):
    l=[]
    for i in range(len(msg)):
        l.append(cosine_distance_countvectorizer_method(msg.translated_message.iloc[i], corpus)*100)
    msg['terrorist_content_similarity'] = l
    return msg

def detect_hastags(msg):
    hasht=[]
    for i in range(len(msg)):
        if len(str(msg.message.iloc[i]).split('#'))>1:
            hasht.append(str(msg.message.iloc[i]).split('#')[1].split(' ')[0])
        else:
            hasht.append('no hashtags')
    msg['hashtags'] = hasht
    return msg

def hastags_preprocessing(msg): 
    l=[]
    for i in range(len(msg)):
        x=( re.sub("[^a-zA-Z]", " ",str(msg.hashtags.iloc[i])))
        x=re.sub(' +', ' ', x)
        m=wordninja.split(x)
        h=''
        for j in range(len(m)):
            h+= m[j]+' '
        #print(h)
        l.append(h.strip())
    msg['hashtags'] = l
    return msg

def hashtags_content_similarity(msg, corpus):
    l=[]
    for i in range(len(msg)):
        if msg.hashtags.iloc[i] != 'no hashtags':
            l.append(cosine_distance_countvectorizer_method(str(msg.hashtags.iloc[i]), corpus)*100)
        else:
            l.append(0)
    msg['hashtags_terrorist_similarity'] = l
    return msg

def contextual_analysis_telegram(messages, node_dict,corpus):
    messages = messages_preprocessing(messages, node_dict)
    messages = detectLanguge(messages)
    messages = translateToEnglish(messages)
    messages = detect_hastags(messages)
    messages = hastags_preprocessing(messages)
    messages = content_similitarity(messages,corpus)
    messages = hashtags_content_similarity(messages, corpus)
    messages = sentimental_analysis_telegram(messages)
    return messages

def sentimental_analysis_telegram(data):    
    data = sentimental_analysis_features(data)
    data["terrorist_suggestion"] = 0
    data["terrorist_suggestion"][(data["terrorist_content_similarity"]>3) | (data["hashtags_terrorist_similarity"]>0)] = 1
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==1) & (data["polarity"] <= -0.1) & (data["subjectivity"]>=0.6)]= "Negative opinion"
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==1) & (data["polarity"] <= -0.1) & (data["subjectivity"]<0.6)]= "Negative fact"
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==1) & (data["polarity"] < 0.1) & (data["polarity"] > -0.1)]= "Neutral"
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==1) & (data["polarity"] >= 0.1) & (data["subjectivity"]<=0.5)]= "Positive opinion"
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==1) & (data["polarity"] >= 0.1) & (data["subjectivity"]>0.5)]= "Positive opinion"
    data["terrorist_suggestion"][(data["terrorist_suggestion"]==0)] = "Don´talk about terrorism" 
    return data

def sentimental_analysis_features_telegram(data):
	corpus =[]
	polarities=[]
	subjectivities=[]
	for tweet in data.translated_message:
		corpus.append(TextBlob(tweet.lower()))
	for i in range(len(corpus)):
		polarities.append(corpus[i].polarity)
		subjectivities.append(corpus[i].subjectivity)
	data['polarity']= polarities
	data['subjectivity']= subjectivities
	return data


