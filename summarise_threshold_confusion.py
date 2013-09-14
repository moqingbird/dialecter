from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db
tables=db.collection_names()
rl={"NI":0,"COR":1,"BRIS":2,"CORN":3,"ABN":4,"BRAD":5,"BRGT":6,"BRNM":7,"BRUM":8,"CANT":9,"CAR":10,"DUB":11,"DUND":12,"EDB":13,"ESX":14,"GAL":15,"GLAS":16,"HULL":17,"LEED":18,"LEIC":19,"LINC":20,"LVP":21,"MANC":22,"NEWC":23,"NORW":24,"NTHM":25,"OXF":26,"PORT":27,"YORK":28,"SHEF":29,"SOUTH":30,"STAN":31,"SURY":32,"UNKNOWN":33}

pr_file=open("precision_recall.csv","w")
pr_file.write("Threshold,Precision,Recall\n")
roc_file=open("roc.csv","w")
roc_file.write("Threshold,TP,FP\n")
unknown_index=rl["UNKNOWN"]
for table in tables:
   if table.startswith("confusion_threshold_"):
     print(table)
     rec_cur=db[table].find()
     recs=[rec for rec in rec_cur]
     precision=[0 for i in range(len(recs))]
     recall=[0 for i in range(len(recs))]
     column_totals=[0 for i in range(len(recs))]
     total_correct=0
     total_wrong=0
     total_items=0
     tp=[0 for i in range(len(recs))]
     for rec in recs:
       rec_correct=rec["totals"][rl[rec["_id"]]]
       total_correct+=rec_correct
       rec_sum=sum(rec["totals"])
       rec_wrong=rec_sum-rec_correct-rec["totals"][unknown_index]
       total_wrong+=rec_wrong
       total_items+=rec_sum
       recall[rl[rec["_id"]]]=0
       if rec_sum > 0:
          recall[rl[rec["_id"]]]=(rec_correct/float(rec_sum))*100
       column_totals=[column_totals[i]+rec["totals"][i]  for i in range(len(recs))]
       tp=[tp[i]+rec["totals"][i] if i==rl[rec["_id"]] else tp[i] for i in range(len(recs))]
     precision=[(tp[i]/float(column_totals[i])*100) if column_totals[i] != 0 else 100 for i in range(len(recs))]
     pr_file.write(table.replace("confusion_threshold_","")+","+str(sum(precision)/float(len(precision)))+","+str(sum(recall)/float(len(recall)))+"\n")
     roc_file.write(table.replace("confusion_threshold_","")+","+str((total_correct/float(total_items))*100)+","+str(((total_wrong)/float(total_items))*100)+"\n")
pr_file.close()
roc_file.close()
