#!/bin/bash
#
# Jose.Salas@Ooma.Com
# 2022/05/2
#
#  Authors: Raj, Greg and Jose'

# Notes:
# Look for UPDATE_HERE <-- These are what yoou need to update for new scripts

# Inputs:
# -  None
# - Example: $0 <-- Our Name

# Process:
# - Loop through directory of files: Extractinator-data-*
# - - Loop through each file - looking for the Band_Item used (field X)
# - - - Push up MyxID (field 1) with the Band_Item (field X) into Graphite
# - - - - Update our log with successful completion
# - - - - - $0.log
# - - - - - - Extractinator-data-<epoc>.csv:Uploaded
#
# - Update our script stat's to the Graphite Server
# - - Housekeeping, Last Run, Exit State (Uploaded, # MyxID's Processed)

###
#
# Function declarations
#
unset _NeedEchoBackslashC_

[ "`echo -n ff`" = "ff" ] || _NeedEchoBackslashC_=1

Echo()
{
  if [ "$_NeedEchoBackslashC_" ]
  then
    echo "$*\\c"
  else
    echo -n "$*"
  fi
} #End of - Echo()

PrepScriptLog()
{
  # Prep our work area
  cd ${ScriptDir}

  # Check if the log file exists
  if [ -f ./${ScriptNameLog} ] ; then
    echo "- - File Exists: ${ScriptNameLog} file"
  else
    echo "- - Created: ${ScriptNameLog} file"
    touch ./${ScriptNameLog}
  fi

}


#####
#
# Main

  # Start: Defaults - Set some defaults - update these as needed
  CustNum="1" # Customer Number

  echo " "
  EpocDate=`date +%s`
  StartDate=`date`
  echo "Started on (Date): $StartDate"
  echo "- Epoch Timestamp: $EpocDate"

  # The name of the running script
  ScriptName=`basename $0`
  ScriptNameLog="${ScriptName}.log"
  ScriptNameGraphiteUpload="${ScriptName}.upload"
  echo "- Script Running : $ScriptName"
  echo "- - Script Log   : $ScriptNameLog"

  ScriptDir="/scratch/customer/${CustNum}/LMS_Data/scripts"
  echo "- - Script Dir   : $ScriptDir"

  ProcessedDir="/scratch/customer/${CustNum}/LMS_Data/processed"
  echo "- - Processed Dir: ${ProcessedDir}"
  echo "- -   \"   \"  File: ${ScriptNameGraphiteUpload}-${EpocDate}"

  ExtractinatorDir="/scratch/customer/${CustNum}/LMS_Data/stage"
  echo "- Extractinator  : $ExtractinatorDir"

  Server=`hostname | awk -F"." '{print $1}'`

  GraphiteServer="${Server}"
  GraphitePort="${CustNum}2003"

  echo "- Graphite Server: $GraphiteServer"
  echo "- Graphite Port  : $GraphitePort"

  GitLabServer="https://gitlab.com/ooma_netops/lms/docker"

  echo "- GitLab Server  : ${GitLabServer}"

  GrafanaServer="${Server}"
  GrafanaPort="${CustNum}3000"

  echo "- Grafana Server : http://${GrafanaServer}"
  echo "- Grafana Port   : ${GrafanaPort}"

  # End: Defaults -


  # Prep: Our Log File and Temp File
  echo "- Prepping Log Area for work"
  PrepScriptLog # Broke off to it's own method - just in case

  echo " "
  echo "Looping through Extractinator Files:"
  echo "========================================================================================"
  cd ${ExtractinatorDir}

  Total_Number_Files=`ls Extractinator-data-* | wc -l | awk -F" " '{print $1}'`
  Current_File=0

  # Loop through All the Extractinator Files
  for File in `ls Extractinator-data-*`
  do
    Current_File=`expr ${Current_File} + 1`
    # Working on each $File
    echo "--------------------------------------------------------------------------------------"
    Echo "- ${File} ("

    # Get the File Epoch (Exanmple: Extractinator-data-1650419245.csv)
    File_Epoc=""; File_Epoc=`echo ${File} | awk -F"[-.]" '{print $3}'` # Don't update this
    File_Date=`/bin/date -d @${File_Epoc}`
    echo "${File_Date}): File ${Current_File} of ${Total_Number_Files}"

    # See if it's already in our log
    File_Exists=""; File_Exists=`grep "^${File}:Uploaded$" ${ScriptDir}/${ScriptNameLog}`

    if [ "${File_Exists} " = " " ] ; then
      Echo "-- Starting,... "
    else
      echo "Already Uploaded - Skipping"
      continue
    fi

    # Get the Rows - based on the total number of Rows
    Total_Rows=`wc -l ${File} | awk -F" " '{print $1}'`
    Current_Row=1
    echo "Pulled Rows,... "
    Echo "-- -- Parsing Line:"

    # read nm
    Bad_Band_Item_Entries=0; Good_Band_Item_Entries=0    # UPDATE_HERE: REPLACE Your Variables HERE - Example: Band_Item

    # Cover the conditions that we are searching for
    while [ ${Current_Row} -le ${Total_Rows} ]
    do
      Line=""
      Line=`head -${Current_Row} ${File} | tail -1`

      Row=`echo "${Line}" | awk -F"," '{print $1","$2","$17}'` # UPDATE_HERE: Update $2 to whatever field you are looking for

      MyxID=""; MyxID=`echo ${Row} | awk -F"," '{print $1}' | tr -d '"'`
      Data_Timestamp=""; Data_Timestamp=`echo ${Row} | awk -F"," '{print $3}' | sed 's/"//g'`
      Data_Epoc=""; Data_Epoc=`date --date="${Data_Timestamp}" +%s`
      if [ "${MyxID} " = " " ] ; then
        # We should NEVER See this - Previous scripts address this
        # We have an issue - the file may have gone away, or ?
        # echo "ERROR: Failed - MyxID ($MyxID) is no longer available - Noting and Skipping"
        echo " "
        Echo "-- -- -- Error: Failed - MyxID Missing! Empty File? Skipping,...."
        echo "echo \"Housekeeping.Ingestion.Band_Item.Failed 100 ${Data_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        break # Exit this loop and skip to the next file
      fi

      Band_Item=""; Band_Item=`echo ${Row} | awk -F"," '{print $2}'`
      if [ "${Band_Item} " = " " ] ; then
        # echo " "
        # echo "Band_Item is Missing - aka NULL - aka ,, "
        echo "echo \"LMS.Device.Issue.${MyxID}.Band_Item.Null 100 ${Data_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        Bad_Band_Item_Entries=`expr ${Bad_Band_Item_Entries} + 1`
        Echo "!"
        Current_Row=`expr ${Current_Row} + 1`
        continue
      fi

      Band_Item=""; Band_Item=`echo ${Row} | awk -F"," '{print $2}' | tr -d '"'`
      if [ "${Band_Item} " = " " ] ; then
        # We have a malformed (EMPTY) Band_Item entry - it should not be blank for this data type - aka ""
        echo "echo \"LMS.Device.Issue.${MyxID}.Band_Item.Malformed 100 ${Data_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        # echo " "
        # echo "Band_Item is Blank - aka EMPTY - aka doublequote thing "
        Bad_Band_Item_Entries=`expr ${Bad_Band_Item_Entries} + 1`
        Echo "x"
        Current_Row=`expr ${Current_Row} + 1`
        continue
      else
        # Convert any "spaces" to "underscores"
        Band_Item_Converted=""
        Band_Item_Converted=`echo "${Band_Item}" | tr ' ' '_'`
        Band_Item=${Band_Item_Converted}
        # We are good - let's update the details
        Echo "."
        echo "echo \"LMS.Device.MyxID.${MyxID}.Band_Item.${Band_Item} 100 ${Data_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        Good_Band_Item_Entries=`expr ${Good_Band_Item_Entries} + 1`
      fi

      Current_Row=`expr ${Current_Row} + 1`
    done

    # Update the Good and Bad Entries - Note: There were no bad MyxID's - so the totals will match up
    echo " "

    AllBand_ItemCategories=""; AllBand_ItemCategories=`cat ${File} | awk -F"," '{print $2}' | tr -d '"' | tr ' '  '_' | sort | uniq` # UPDATE_HERE: Make this your field - Example: $2
    for SingleCategory in `echo ${AllBand_ItemCategories}`
    do
      Search_String=""; Search_String=`echo ${SingleCategory} | tr '_' ' '`
      Amount=`cat ${File} | awk -F"," '{print $2}' | grep "\"${Search_String}\"" | wc -l`                           # UPDATE_HERE: Make this your field - Example: $2
      echo " - Field Value: ${SingleCategory} = ${Amount} Entries"
      echo "echo \"LMS.Totals.Device.Band_Item.Category.${SingleCategory} ${Amount} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    done

    echo "echo \"LMS.Totals.Device.Band_Item.Totals ${Good_Band_Item_Entries} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    echo " - Field Value Total: Good = ${Good_Band_Item_Entries} Entries"
    echo "echo \"LMS.Totals.Issues.Band_Item.Malformed ${Bad_Band_Item_Entries} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    echo " - Field Value Total: Bad = ${Bad_Band_Item_Entries} Entries"
    echo "${File}:Uploaded" >> ${ScriptDir}/${ScriptNameLog}

    echo "- - Upload Preparation Completed"
  done

  echo " "
  echo "Uploading Band_Item Data to Graphite"
  OurPushStartDate=`/bin/date`
  echo "- Pushing: (Will take a while - initially - then it's fast) on ${OurPushStartDate}"

  #exit 1  # Uncomment while testing
  chmod +x ${ScriptDir}/${ScriptNameGraphiteUpload}
  python3 /scratch/customer/${CustNum}/LMS_Data/scripts/Data_Ingestinator.py ${ScriptDir}/${ScriptNameGraphiteUpload}
  OurPushEndDate=`/bin/date`
  echo "- - Completed upload to Graphite on ${OurPushEndDate}"

  # Cleanup
  echo " "
  echo "Cleaning up: "
  echo "- Moving ${ScriptNameGraphiteUpload} to ../processed/"
  \mv ${ScriptDir}/${ScriptNameGraphiteUpload} ${ProcessedDir}/${ScriptNameGraphiteUpload}-${EpocDate}
  echo "- Compressing (gzip -9): ${ScriptNameGraphiteUpload}-${EpocDate}"
  gzip -9 ${ProcessedDir}/${ScriptNameGraphiteUpload}-${EpocDate}

  # Custom extra checks here
  # - Add your extra checks in here
  echo " "
  echo "Misc. Items:"
  echo " "
  echo "- Done."

  echo " "
  EndDate=`date`
  echo "Started on (Date)  : $StartDate"
  echo "Completed on (Date): $EndDate"
  echo "Done."
