#!/bin/bash
#
# Jose.Salas@Ooma.Com
# 2022/05/10
#
#  Authors: Raj, Greg and Jose'

# Notes:
# Look for UPDATE_HERE <-- These are what you need to update for new scripts

# Inputs:
# -  None
# - Example: $0 <-- Our Name

# Process:
# - Loop through directory of files: Extractinator-data-*
# - - Loop through each file - looking for the Software_Version used (field X)
# - - - Push up MyxID (field 1) with the Software_Version (field X) into Graphite
# - - - - Update our log with successful completion
# - - - - - $0.log
# - - - - - - Extractinator-data-<epoc>.csv:Uploaded
# - - - Keep track of SW versions
# - - - - $0.versions
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

PrepSofwareVersionLog()
{
  # Prep our work area
  cd ${ScriptDir}

  # Check if the log file exists
  if [ -f ./${SoftwareVersionLog} ] ; then
    echo "- - File Exists: ${SoftwareVersionLog} file"
  else
    echo "- - Created: ${SoftwareVersionLog} file"
    touch ./${SoftwareVersionLog}
  fi
  # Read SW version log into an array
  readarray -t Software_Version_Array < ${SoftwareVersionLog}
  
  File_Software_Version_Number=${#Software_Version_Array[@]}
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
  SoftwareVersionLog="${ScriptName}.versions"
  ScriptNameGraphiteUpload="${ScriptName}.upload"
  echo "- Script Running : $ScriptName"
  echo "- - Script Log   : $ScriptNameLog"
  echo "- - SW Versions Log   : $SoftwareVersionLog"

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
  PrepSofwareVersionLog

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
    Bad_Software_Version_Entries=0; Good_Software_Version_Entries=0    # UPDATE_HERE: REPLACE Your Variables HERE - Example: Software_Version

    # Cover the conditions that we are searching for
    while [ ${Current_Row} -le ${Total_Rows} ]
    do
      Line=""
      Line=`head -${Current_Row} ${File} | tail -1`

      Row=`echo "${Line}" | awk -F'","' '{print $1","$20}'` # UPDATE_HERE: Update $20 to whatever field you are looking for

      MyxID=""; MyxID=`echo ${Row} | awk -F"," '{print $1}' | tr -d '"'`
      if [ "${MyxID} " = " " ] ; then
        # We should NEVER See this - Previous scripts address this
        # We have an issue - the file may have gone away, or ?
        # echo "ERROR: Failed - MyxID ($MyxID) is no longer available - Noting and Skipping"
        echo " "
        Echo "-- -- -- Error: Failed - MyxID Missing! Empty File? Skipping,...."
        echo "echo \"Housekeeping.Ingestion.Software_Version.Failed 100 ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        break # Exit this loop and skip to the next file
      fi

      Software_Version=""; Software_Version=`echo ${Row} | awk -F"," '{print $2}'`
      if [ "${Software_Version} " = " " ] ; then
        # echo " "
        # echo "Software_Version is Missing - aka NULL - aka ,, "
        echo "echo \"LMS.Device.Issue.${MyxID}.Software_Version.Null 100 ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        Bad_Software_Version_Entries=`expr ${Bad_Software_Version_Entries} + 1`
        Echo "!"
        Current_Row=`expr ${Current_Row} + 1`
        continue
      fi

      Software_Version=""; Software_Version=`echo ${Row} | awk -F"," '{print $2}' | tr -d '"'`
      if [ "${Software_Version} " = " " ] ; then
        # We have a malformed (EMPTY) Software_Version entry - it should not be blank for this data type - aka ""
        echo "echo \"LMS.Device.Issue.${MyxID}.Software_Version.Malformed 100 ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        # echo " "
        # echo "Software_Version is Blank - aka EMPTY - aka doublequote thing "
        Bad_Software_Version_Entries=`expr ${Bad_Software_Version_Entries} + 1`
        Echo "x"
        Current_Row=`expr ${Current_Row} + 1`
        continue
      else
        # Convert any "spaces" to "underscores"
        Software_Version_Converted=""
        Software_Version_Converted=`echo "${Software_Version}" | tr ' :.' '_' | tr -s '_'`
        Software_Version=${Software_Version_Converted}
        # We are good - let's update the details
        # See if it's already in our SW version log. If not, appeand to list
        if [[ ! "${Software_Version_Array[*]}" =~ "${Software_Version}" ]]; then
          File_Software_Version_Number="`expr ${File_Software_Version_Number} + 1`"
          echo "${File_Software_Version_Number},${Software_Version}" >> ${ScriptDir}/${SoftwareVersionLog}
          Software_Version_Array+="${Software_Version}"
        fi
        Echo "."
        echo "echo \"LMS.Device.MyxID.${MyxID}.Software_Version.${Software_Version} 100 ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        echo "echo \"LMS.Device.MyxID.${MyxID}.Software_Version.Current ${File_Software_Version_Number} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
        Good_Software_Version_Entries=`expr ${Good_Software_Version_Entries} + 1`
      fi

      Current_Row=`expr ${Current_Row} + 1`
    done

    # Update the Good and Bad Entries - Note: There were no bad MyxID's - so the totals will match up
    echo " "

    All_Software_Version_Categories=""; All_Software_Version_Categories=`cat ${File} | awk -F'","' '{print $20}' | tr -d '"' | tr ' :.'  '_' | tr -s '_' | sort | uniq` # UPDATE_HERE: Make this your field - Example: $2
    for SingleCategory in `echo ${All_Software_Version_Categories}`
    do
      Amount=`cat ${File} | awk -F'","' '{print $20}'| tr -d '"' | tr ' :.'  '_' | tr -s '_' | grep ${SingleCategory} | wc -l`                           # UPDATE_HERE: Make this your field - Example: $20
      echo " - Field Value: ${SingleCategory} = ${Amount} Entries"
      echo "echo \"LMS.Totals.Device.Software_Version.Category.${SingleCategory} ${Amount} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    done

    echo "echo \"LMS.Totals.Device.Software_Version.Totals ${Good_Software_Version_Entries} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    echo " - Field Value Total: Good = ${Good_Software_Version_Entries} Entries"
    echo "echo \"LMS.Totals.Issues.Software_Version.Malformed ${Bad_Software_Version_Entries} ${File_Epoc}\" | nc ${GraphiteServer} ${GraphitePort}" >> ${ScriptDir}/${ScriptNameGraphiteUpload}
    echo " - Field Value Total: Bad = ${Bad_Software_Version_Entries} Entries"
    echo "${File}:Uploaded" >> ${ScriptDir}/${ScriptNameLog}

    echo "- - Upload Preparation Completed"
  done

  echo " "
  echo "Uploading Software_Version Data to Graphite"
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
