# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#
from Products.MeetingCommunes.browser.overrides import (
    MCItemDocumentGenerationHelperView,
    MCMeetingDocumentGenerationHelperView,
)
from collective.contact.plonegroup.utils import get_organizations


class MCBaseDocumentGenerationHelperView(object):

    def getIdeaAssembly(self, filter):
        '''return formated assembly
           filer is 'present', 'excused', 'procuration', 'absent' or '*' for all
           This method is used on template
        '''
        if self.context.meta_type == 'Meeting':
            assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '')
        else:
            assembly = self.context.getItemAssembly().replace('<p>', '').replace('</p>', '')
        assembly = assembly.split('<br />')
        res = []
        status = 'present'
        for ass in assembly:
            # ass line "Excusé:" is used for define list of persons who are excused
            if ass.find('xcus') >= 0:
                status = 'excused'
                continue
            # ass line "Procurations:" is used for defined list of persons who recieve a procuration
            if ass.upper().find('PROCURATION') >= 0:
                status = 'procuration'
                continue
            # ass line "Absents:" is used for define list of persons who are excused
            if ass.upper().find('ABSENT') >= 0:
                status = 'absentee'
                continue
            if filter == '*' or status == filter:
                res.append(ass)
        return res

    # TODO Totally inefficient methods used in PODTemplates that need to be refactored... some day

    def getCountDptItems(self, meeting=None, dptid='', late=False):
        long = 0
        listTypes = ['late'] if late else ['normal']
        for sublist in meeting.adapted().getPrintableItemsByCategory(listTypes=listTypes):
            if sublist[0].id == dptid:
                long = len(sublist) - 1  # remove categories
                return long
        return long

    def getDepartment(self, group):
        # return position, title and class for department
        cpt_dpt = self.getDptPos(group.id)
        res = '%d. %s' % (cpt_dpt, group.Title())
        return res

    def getDptForItem(selg, groupid):
        # return department
        res = ''
        groups = get_organizations()
        for group in groups:
            acronym = group.get_acronym()
            if acronym.find('-') < 0:
                res = group.id
            if group.id == groupid:
                break
        return res

    def getDptPos(self, groupid):
        # return department position in active groups list
        res = ''
        groups = get_organizations()
        cpt_dpt = 0
        for group in groups:
            acronym = group.get_acronym()
            if acronym.find('-') < 0:
                cpt_dpt = cpt_dpt + 1
            if group.id == groupid:
                break
        res = cpt_dpt
        return res

    def getItemPosInCategorie(self, item=None, late=False):
        if not item:
            return ''
        meeting = item.getMeeting()
        pg = item.getProposingGroup()
        if late:
            cpt = self.getItemPosInCategorie(item, False)
        else:
            cpt = 1
        listTypes = ['late'] if late else ['normal']
        for sublist in meeting.adapted().getIDEAPrintableItemsByCategory(listTypes=listTypes):
            for elt in sublist[1:]:
                if elt.id == item.id:
                    break
                if elt.getProposingGroup() == pg:
                    cpt = cpt + 1
        return cpt

    def getServiceIsEmpty(self, groupid, meeting=None, late=False):
        listTypes = ['late'] if late else ['normal']
        for sublist in meeting.adapted().getIDEAPrintableItemsByCategory(listTypes=listTypes):
            if sublist[0].id == groupid:
                isEmpty = len(sublist) <= 1
                return isEmpty
        return True

    def getServicePos(self, group, meeting=None, late=False):
        # return service position in active groups list incremented by item for department
        groupid = group.id
        cpt_srv = 0
        groups = get_organizations()
        for gr in groups:
            acronym = gr.get_acronym()
            if acronym.find('-') >= 0:
                # only increment if no empty service and not current group
                if (gr.id != groupid) and (not self.getServiceIsEmpty(gr.id, meeting, late)):
                    cpt_srv = cpt_srv + 1
            else:  # new department, reset numbering
                cpt_srv = 1
            if gr.id == groupid:
                break
        dptid = self.getDptForItem(group.id)
        cpt_srv = cpt_srv + self.getCountDptItems(meeting, dptid, late)
        return cpt_srv


class MIDEAItemDocumentGenerationHelperView(
    MCBaseDocumentGenerationHelperView, MCItemDocumentGenerationHelperView
):
    """Specific printing methods used for item."""


class MIDEAMeetingDocumentGenerationHelperView(
    MCBaseDocumentGenerationHelperView, MCMeetingDocumentGenerationHelperView
):
    """Specific printing methods used for meeting."""
