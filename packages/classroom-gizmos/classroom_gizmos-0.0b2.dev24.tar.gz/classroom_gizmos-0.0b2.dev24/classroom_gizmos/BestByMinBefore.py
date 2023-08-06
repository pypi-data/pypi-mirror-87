''' calc minutes before for BestBuy, In-class, etc. questions
returns a string that is the perl code fragment for specific cases.xs
2020-09-25 /CS/ revised wording in getCCode() prompts.'''
## ----- Time-stamp: <2020-09-18T08:36:44.441669-04:00 hedfp> -----

 
from __future__ import absolute_import, division, print_function, unicode_literals
 
import time
from math import sqrt
 
##############################################

### Default last days for classes:
duedates = { 'PHYS250.001':'2020-12-17 23:59:00', 'PHYS251': '2020-12-17 23:59:00',
             'PHYS250.002':'2020-12-17 23:59:00'}

### Added hours to end of full points time for safety margin.
nudge=1.9   ## h added to be 'safe'

### Usual times for credit to decrease
InC_hours = 12
BBP_hours = 24*7

### Usual minimum credit as fraction of full credit
minCreditF = 0.2

### Some time conversions
hr = 3600  ## 1 hour is 3660 s
day = 86400 ## 1 day is 87840 s
week = 604800 ## 1 week is 604880 s

def BB():
    print( '\nFunctions in BestByMinBefore:\n')
    print( 'decCredit( decStart, hoursToMinimum=BBP_hours, fullCreditSubs=5, minCreditSubs=10,')
    print( '          minCreditFraction=minCreditF, assignmentDue=duedates[ "PHYS250.001"]),')
    print( '          nudge=1.9')
    print()
    print( 'BBPdecCredit( decStart, hoursToMinimum=7*24)')
    print()
    print( 'InCdecCredit( decStart, hoursToMinimum=24)')
    print()
    print( 'HWdecCredit( )')
    print()
    print( 'getCCode() --> prompts user for parameter values.')
    print()
    print( '\n Helpers:')
    print( 'localTimeToGMTepoch( localTime)')
    print()
    print( 'minBeforeToLocal( minBefore, assignmentDue=duedates[ "PHYS250.001"])')
    
    

def localTimeToGMTepoch( localTime):
    '''
    

    Parameters
    ----------
    localTime : a date string in format "%Y-%m-%d %H:%M" or "%Y-%m-%d %H:%M:%S"
            ( yyyy-mm-dd hh:mm  or yyyy-mm-dd hh:mm:ss  )
        for a local (Eastern time) time

    Returns
    -------
    GMT epoch of that time
    '''
    
    try:
        tuple = time.strptime( localTime, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            tuple = time.strptime( localTime, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise
            
    # print( 'DBug: tuple: {}'.format( tuple))
    
    epochFromLocal = time.mktime( tuple)  ## seconds since 1970-01-01 00:00:00 GMT
    # print( 'DBug: epoch for {} is {}'.format(
    #     localTime, epochFromLocal))

    return epochFromLocal

def minBeforeToLocal( minBefore, assignmentDue=duedates[ 'PHYS250.001']):
    '''
    Convert minutes before assignment is due to a date.

    Parameters
    ----------
    minBefore : integer
        minutes before the assignment is due.
    assignmentDue : string
        date/time string when assignment is due.
    Returns
    -------
    date/time string for minBefore minutes before assignmentDue

    '''
    beforeDueEpoch = localTimeToGMTepoch( assignmentDue) - minBefore*60  ## in seconds
    
    return time.asctime( time.localtime( beforeDueEpoch))


def decCredit( decStart, hoursToMinimum=BBP_hours, fullCreditSubs=5, minCreditSubs=10,
              minCreditFraction=minCreditF, assignmentDue=duedates[ 'PHYS250.001'], nudge=nudge):
    '''
    General decreasing credit perl string generator.

    Parameters
    ----------
    decStart : (a date string in format "%Y-%m-%d %H:%M:%S")
        This is the date/time when the credit for an correct answer starts to decrease.
        if the string is empty or parameter == None, then credit does not decrease
          with time.
        A date string, example:
            2020-08-31 23:59:00
    hoursToMinimum : float
        Number of hours to decrease before minimum credit.
        The default is 7*24.
    fullCreditSubs : integer
        The number of submissions that receive full credit.
        if zero or negative, then credit does not decrease with submissions.
    minCreditSubs : integer
        The number of submissions at which the decrease reaches the minimum
        credit for a correct answer.
        Must be greater than fullCreditSubs if fullCreditSubs is positive.
        Ignored if fullCreditSubs is zero or negative.
    minCreditFraction : float
        Fraction of the points received for correct answer with minCreditSubs
        submissions. If the credit decreases with time and submissions, then
        sqrt(minCreditFraction) is applied to time decrease and also to
        submission increase. The result is that after time runs out and
        submissions reaches minCreditSubs then the credit is reduced by this
        amount.
    assignmentDue: (a date string in format "%Y-%m-%d %H:%M:%S")
        due date/time for WebAssign assignment. This is the time that
        minute differences are calculated from.
    nudge: (in hours) the time to add to the decStart to allow for differences in
        time zones or computer clocks.

    Returns
    -------
    perl string to calculate the points, decreasing with time and with submissions

    '''
    
    '''
    There are three times needed:
        1. the time the assignment is due 
           ( assignmentDue --> epochDue --> zero minutes before due
        2. the time the credit starts decreasing 
           ( decStart) --> decMinutes = ( epochDue - epochStart)/60 ## minutes before due
        3. the time the credit has reached its minimum.
            ( decStart + hoursToMinimum) --> 
              endMinutes = ( epochDue - epochStart)/60 - hoursToMinimum*60 ## minutes before due
    
   '''
    

    outPerl = ''   ## string built up for output
   
    ### Determine factors for decrease with submissions and with time
    timeMult = 0.0
    subsMult = 0.0
    if decStart=='' or decStart==None:
        if fullCreditSubs<=0.0:
            print( 'ERROR neither decreases with time nor with submissions.')
            return None
        else:
            subsMult = minCreditFraction
    else:
        if fullCreditSubs<=0.0:
            timeMult = minCreditFraction
        else:
            timeMult = round( sqrt( minCreditFraction), 3)
            subsMult = round( minCreditFraction/timeMult, 3)
    # print( 'DBug: timeMult {}, subsMult {}'.format(
    #          timeMult, subsMult))
           
    if not ( decStart=='' or decStart== None):  ## if decrease with time.
    
    ## generate time decreasing part
        epochDue = localTimeToGMTepoch( assignmentDue)           ## in seconds
        epochStart = localTimeToGMTepoch( decStart) + nudge*3600 ## in seconds
        epochMinimum = epochStart + hoursToMinimum*3600          ## in seconds
        
        # print( 'DBug: epochDue {}, epochStart {}, epochMinimum {}'.format(
        #         epochDue, epochStart, epochMinimum))
        # print( 'DBug: (in s) Due-Start {}, Due-Minimim {}, Minimum-Start {}'.format(
        #         epochDue-epochStart, epochDue-epochMinimum, epochMinimum-epochStart))
        # print( 'DBug: (in min) Due-Start {}, Due-Minimim {}, Minimum-Start {}'.format(
        #         (epochDue-epochStart)/60, (epochDue-epochMinimum)/60,
        #         (epochMinimum-epochStart)/60))
        # print( 'DBug: (in hr) Due-Start {}, Due-Minimim {}, Minimum-Start {}'.format(
        #         (epochDue-epochStart)/3600, (epochDue-epochMinimum)/3600,
        #         (epochMinimum-epochStart)/3600))
        # print( 'DBug: (in day) Due-Start {}, Due-Minimim {}, Minimum-Start {}'.format(
        #         (epochDue-epochStart)/day, (epochDue-epochMinimum)/day,
        #         (epochMinimum-epochStart)/day))
        
        decMinutes = round( ( epochDue - epochStart)/60) ## minutes before due, when decrease starts
        endMinutes = round( ( epochDue - epochMinimum)/60) ## minumtes before due, when decrease ends
        
        # print( 'DBug decMinutes: {}, endMinutes: {}'.format(
        #        decMinutes, endMinutes))
        
        outPerl = "&cs9(-&beforeDue('minutes'),{},{},{})".format(
            -decMinutes, -endMinutes, timeMult)
        
        print( '\nAssignment is Due         {}, nudge is {} h.'.format(
              minBeforeToLocal( 00, assignmentDue), nudge))
        print( 'Decreasing start specified: {} Decrease time: {} h or {:0.2f} d'.format(
               decStart, hoursToMinimum, hoursToMinimum/24))
        print( 'Decreasing credit starts ',
              minBeforeToLocal( decMinutes, assignmentDue))
        print( 'Decreasing credit ends {}, to {}% credit, {}% dec. with subs.'.format(
              minBeforeToLocal( endMinutes, assignmentDue),
              timeMult*100, subsMult*100))
        
        ## add '*' if there is a submissions decrease part or finish line.
        if fullCreditSubs>0:
            outPerl = outPerl + '*\n'
        else:
            outPerl = outPerl + '*$POINTS</eqn>'
            
        # print( 'DBug: outPerl:\n{}'.format( outPerl))
    if not fullCreditSubs<=0:
        outPerl = outPerl + '&cs9($RESPONSE_NUM,{},{},{})*$POINTS</eqn>'.format(
                fullCreditSubs, minCreditSubs, subsMult)
    print( '\n++++++++++++++ Copy and Paste conditional code starting on next line.' +\
            '+++++++++++')
    print( '''<eqn>sub cs9{my($tn,$t1,$t2,$mn)=@_;
my $f=((1-$mn)*$tn+$mn*$t1-$t2)/($t1-$t2);
if($tn<=$t1){$f=1}
if($tn>=$t2){$f=$mn}
return $f}''')
    
    print( outPerl)
    # return outPerl


def BBPdecCredit( decStart, hoursToMinimum=7*24):
    '''
    Best By Prep decreasing credit
    Returns perl string that reduces credit after decStart.

    Convenience function that is equivalent to
      decCredit( decStart, hoursToMinimum, fullCreditSubs=5, minCreditSubs=10,
              minCreditFraction=0.2, assignmentDue=duedates[ 'PHYS250.001'], nudge)
        

    Parameters
    ----------
    decStart : (a date string in format "%Y-%m-%d %H:%M:%S")
        A date string, example:
            2020-08-31 23:59:00
    hoursToMin : TYPE
        Number of hours to decrease before minimum credit.

    Returns
    -------
    perl string to calculate the points, decreasing with time and with submissions

    '''
    decCredit( decStart, hoursToMinimum, fullCreditSubs=5, minCreditSubs=10,
              minCreditFraction=0.2, assignmentDue=duedates[ 'PHYS250.001'])

def InCdecCredit( decStart, hoursToMinimum=24):
    '''
    in class exercise
    Returns perl string that reduces credit after decStart.
    
    Convenience function that is equivalent to
      decCredit( decStart, hoursToMinimum, fullCreditSubs=0, minCreditSubs=10,
              minCreditFraction=0.2, assignmentDue=duedates[ 'PHYS250.001'], nudge)


    Parameters
    ----------
    decStart : (a date string in format "%Y-%m-%d %H:%M:%S")
        A date string, example:
            2020-08-31 23:59:00
    hoursToMin : TYPE
        Number of hours to decrease before minimum credit.

    Returns
    -------
    perl string to calculate the points, decreasing with time only.

    '''

    decCredit( decStart, hoursToMinimum, fullCreditSubs=0, minCreditSubs=10,
              minCreditFraction=0.4, assignmentDue=duedates[ 'PHYS250.001'])


def HWdecCredit( ):
    '''
    Home Work assignment, numerical answer

    Returns perl string that reduces credit after 5 submissions.
    
    Convenience function that is equivalent to
      decCredit( decStart, hoursToMinimum, fullCreditSubs=0, minCreditSubs=10,
              minCreditFraction=0.2, assignmentDue=duedates[ 'PHYS250.001'], nudge)
    

    Returns
    -------
    perl string to calculate the points, decreasing with time only.
    '''

    decCredit( '')

def is_number(s):
    '''
    

    Parameters
    ----------
    s : string
        string to check if it can be converted to a number.

    Returns
    -------
    bool
        Returns True if string can be converted to a number.
    Ref: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_datetime(s):
    '''
    Test if string is valid date-time string.
    Parameters
    ----------
    s : string
    Returns
    -------
    Boolean
    '''
    try:
        localTimeToGMTepoch( s) 
        return True
    except :
        return False


def getCCode():
    '''
    Prompts for arguments to decCredit() and then calls it
    to get Perl code for the conditional credit field in WebAssign.

    Returns
    -------
    outputs perl code.

    '''
    due = duedates[ "PHYS250.001"]
    fulldue = ""
    fullsubs = 5
    minsubs = 10
    tfrac = 0.2
    hours = 12
    
    print( '\nNote: Default values are in square brackets.\n Date format is {}'.format(
                due))
    prompt = 'Enter BestBy date, or <return> if credit does not decrease with time:'
    response = input( prompt.strip())
    
    if response == "":
        pass
    elif is_datetime( response):
        fulldue = response
    else:
        print( '{} is not in proper Date Time format.'.format( response))
        return

    
    if not fulldue == "":
        ## ck if due date is default
        prompt = 'Enter WebAssign due date [{}]:'
        response = input( prompt.format( duedates[ "PHYS250.001"])).strip()
    
        if response == "":
            pass
        elif is_datetime( response):
            due = localTimeToGMTepoch( response) 
        else:
            print( '{} is not in proper Date Time format.'.format( response))
            return
        print( 'DBug due: {}'.format( due))
    
        
    

    prompt = 'Enter the number of submissions that receive full credit,\n 0 for all at full credit [{}]:'      
    response = input( prompt.format( fullsubs)).strip()
    
    if response == "":
        pass
    elif response == 'zero' or response == '0':
        fullsubs = 0
        minsubs = 0
        tfrac = 0.4
    elif not is_number( response):
        print( '{} is not a number.'.format( response))
        return
    elif float( response) <= 0.0:
        fullsubs = 0
        minsubs = 0
    elif int( response) > 0:
        fullsubs = int( response)
    else:
        print( 'Did not recognize "{}" for response.'.format( response))
        return
    
    if fullsubs > 0:
        prompt = "Enter number of submissions where credit reaches minimum [{}]:"
        response = input( prompt.format( minsubs)).strip()
        
        if response == "":
            pass
        elif not is_number( response):
            print( '{} is not a number.'.format( response))
            return
        elif int( response) >= fullsubs:
            minsubs = int( response)
        else:
            print( 'Did not recognize "{}" for response.'.format( response))
            return
            
    if fulldue != "":  ## credit decreases with time, need to know how fast.
        prompt = 'Enter number days for credit to decrease to minumum [{:.2f}]:'    
        response = input( prompt.format( hours/24)).strip()
        print('DBug response: {}'.format( response))
        if response == "":
            pass
        elif not is_number( response):
            print( '{} is not a number.'.format( response))
            return
        else:
            hours = float( response)*24
        prompt = 'Enter fractional credit after time and submission limits [{}]:'
        response = input( prompt.format( tfrac)).strip()
        if response == "":
            pass
        elif not is_number( response):
            print( '{} is not a number.'.format( response))
            return
        else:
            tfrac = float( response)
            if tfrac > 1.0 or tfrac < 0.0:
                print( '{} is not a valid fractional decrease.'.format( tfrac))
                return
 

    print( 'DBug: fulldue "{}", due {}, fullsubs {}, minsubs {}, tfrac {}, hours {}'.format(
        fulldue, due, fullsubs, minsubs, tfrac, hours))
    
    print( '_____________  Perl Code Below ++++++++++++++')
    
    decCredit( fulldue, hours, fullsubs, minsubs, tfrac, due)
    return

if __name__=="__main__":
    print( '\nTesting BestByMinBefore.py\n')
    
    decStart = '2020-09-01 23:59'
    print( 'decStart:', decStart)
    
    print( '\ndecCredit:')
    decCredit( decStart)
    
    print( '\nHW:')
    HWdecCredit()
    
    print( '\nInCdecCredit:')
    InCdecCredit( decStart)
    
    print( '\nBBPdecCredit:')
    BBPdecCredit( decStart)
    
    
    
    # test1 = decCredit( '2020-08-21 23:58:00')
    # assert test1=="&cs9(-&beforeDue('minutes'),-169867,-159787,0.447)*\n&cs9($RESPONSE_NUM,5,10,0.447)*$POINTS</eqn>"
    
    