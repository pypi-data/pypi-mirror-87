# coding: UTF-8

"""
This file is part of CFONB.

CFONB is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with CFONB.  If not, see <http://www.gnu.org/licenses/>.
"""
from cfonb.writer.common import write, save, date_format, BR_LINE

"""
 Coryright 2011, Stéphane Planquart <stephane@planquart.com>

 Créer un fichier de virement bancaire compatible avec "la structure des
 fichiers transmis par ETABAC 3 selon la norme CFONB"
 ce module prend en compte le format fourni par CFONB, il peut y avoir des
 différence en fonction de votre banque qui ne respecte pas totalement cette
 norme.
 "Seules les banques peuvent fournir le dessin exact des structures de
 fichier à jours"
"""

class Transfert:
    """
    Transfert example:

    >>> from datetime import date
    >>> d = date(2011,10,14)
    >>> a = Transfert()
    >>> a = a.setEmeteurInfos('2000121','affility','virement de test',503103,2313033,1212,d)
    >>> a.render()
    '0302        200012       14101affility                viremen                   E     503102313033                                                   1212       \\r\\n0802        200012                                                                                    0000000000000000                                          \\r\\n'

    """
    _emeteur = {}   #dict des infos sur l'emeteur du fichier de virement
    total    = 0    #total des virements en centime d'euros
    _content = ""   #contenu du fichier de virement sans le header et le footer

    def __init__(self):
        self.total = 0
        pass

    def setEmeteurInfos(self,num_emeteur, raisonsocial, reference,
                             guichet, num_compte, banque, datevir):
        self._emeteur['num_emetteur']   = str(num_emeteur)
        self._emeteur['raisonsocial']   = raisonsocial
        self._emeteur['reference']      = reference
        self._emeteur['guichet']        = guichet
        self._emeteur['num_compte']     = num_compte
        self._emeteur['banque']         = banque
        self._datevir                   = date_format(datevir)
        return self

    def add(self, reference, raisonsocial, domiciliation,
            guichet, compte, montant, libelle,
            etablissement, balance=''):
        montant        *= 100       #passe le montant en centime d'euros
        self.total     += montant   #ajout le momtant au total des virements
        self._content   = self._add(reference, raisonsocial, domiciliation,
                                    guichet, compte, montant, libelle,
                                    etablissement, balance)
        return self

    def render(self, filename=None):
        return save(self._header(), self._content, self._footer(), filename)

    def _header(self):
        #[zone A]
        content  = "03"
        #[zone B1]
        content += "02"
        #[zone B2] Espace reserve 8 caracteres
        content += write('', 8)
        #[zone B3] numero emetteur (attribue par chaque etablisement 6 caracteres)
        content += write(self._emeteur['num_emetteur'], 6)
        #[zone C1-1] code CCD (virement à échéance "E-3")
        content += write('', 1)
        #[zone C1-2] Espace reserve 6 caracteres
        content += write('', 6)
        #[zone C1-3] date JJMMA
        content += self._datevir;
        #[zone C2] Raison sociale du donneur d'ordre (24 caracteres max)
        content += write(self._emeteur['raisonsocial'], 24)
        #[zone D1-1] Reference virement sur 7 caracteres
        content += write(self._emeteur['reference'], 7)
        #[zone D1-2] Espace reserve 17 caracteres
        content += write('', 17)
        #[zone D2-1] Espace reserve 2 caracteres
        content += write('', 2)
        #[zone D2-2] Virement effectue en euro sur 1 caractere
        content += "E";
        #[zone D2-3] Espace reserve 5 caracteres
        content += write('', 5)
        #[zone D3] Code Guichet Emetteur 5 caracteres
        content += write(self._emeteur['guichet'], 5)
        #[zone D4] Numero de compte Emetteur 11 caracteres
        content += write(self._emeteur['num_compte'], 11)
        #[zone E] Espace reserve 16 caracteres
        content += write('', 16)
        #[zone F] Espace reserve 31 caracteres
        content += write('', 31)
        #[zone G1] code etablissement de la banque du donneur d'ordre
        #          5 caracteres
        content += write(self._emeteur['banque'], 5)
        #[zone G2] Espace reserve 6 caracteres
        content += write('', 6)
        content += BR_LINE
        return content

    def _footer(self):
        #[zone A]08 -> Code enregistrement (Entête Total)
        content  = "08"
        #[zone B1]02 -> Nature de l'enregistrement (virement à vue )
        content += "02"
        #[zone B2]8 espaces
        content += write("", 8)
        #[zone B3] numéro émetteur (numéro attribué par chaque établissement à son client émetteur)
        content += write(self._emeteur['num_emetteur'], 6)
        #[zone C1]Réservée 12 caractères
        content += write("", 12)
        #[zone C2]Réservée 24 caractères
        content += write("", 24)
        #[zone D1]Réservée 24 caractères
        content += write("", 24)
        #[zone D2]Réservée 8 caractères
        content += write("", 8)
        #[zone D3]Réservée 5 caractères
        content += write("", 5)
        #[zone D4]Réservée 11 caractères
        content += write("", 11)
        #[zone E]Montant : les 16 positions contiennent le montant centimes
        #                  compris (00 s'il y a lieu) cadré à droite , non signé, complété à gauche par des zéros
        content += write(self.total, 16, rpad=True, fill_char='0')
        #[zone F]Réservée 31 caractères
        content += write("", 31)
        #[zone G1]Réservée 5 caractères
        content += write("", 5)
        #[zone G2]Réservée 6 caractères
        content += write("", 6)
        content += BR_LINE
        return content

    def _add(self,reference, raisonsocial,domiciliation,
            guichet, compte, montant, libelle,
            etablissement, balance=''):
        #[zone A]06 -> Code enregistrement (Entête destinataire)
        content  = "06"
        #[zone B1]02 -> Nature de l'enregistrement (virement à vue )
        content += "02"
        #[zone B2]Espace réservé 8 caractères
        content += write("", 8)
        #[zone B3] numéro émetteur (numéro attribué par chaque établissement à
        #          son client émetteur)
        content += write(self._emeteur['num_emetteur'], 6)
        #[zone C1] référence (numéro facture par exemple) 12car
        content += write(reference, 12)
        #[zone C2] raison social du destinataure (24 caractères max)
        content += write(raisonsocial, 24)
        #[zone D1] domiciliation : désignation en clair du guichet et de la
        #         banque de domiciliataire (facultatif) sur 24  caractères maxi
        content += write(domiciliation, 24)
        #[zone D2] balance des paiements sur 8 caractères
        #         (réservé pour les salaires et pension)
        content += write("", 8)
        #[zone D3] Code Guichet 5 caractères
        content += write(guichet, 5)
        #[zone D4] Numéro de compte sur 11 caractères
        content += write(compte, 5)
        #[zone E]Montant : les 16 positions contiennent le montant centimes
        #        compris (00 s'il y a lieu) cadré à droite , non signé, complété à
        #        gauche par des zéros
        content += write(montant, 16, rpad=True, fill_char='0')
        #[zone F]Libellé : 31 caractères à la disposition du client émetteur
        #        pour indication du motif et des références de l'opération
        content += write(libelle, 31)
        #[zone G1]Code établissement destinataire 5 chiffres
        content += write(etablissement, 5)
        #[zone G2]Zone réservée de 6 caractères
        content += write("", 6)
        content += BR_LINE
        return content
