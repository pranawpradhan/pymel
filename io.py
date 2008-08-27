
"""
The io module contains functions relating to files and references.

In particular, the io module contains the functionality of maya.cmds.file. The file command should not be imported into
the default namespace because it conflicts with python's builtin file class. Since the file command has so many flags, 
I decided to kill two birds with one stone: by breaking the file command down into multiple functions -- one for each 
primary flag -- the resulting functions are more readable and allow the file command's functionality to be used directly
within the pymel namespace.   

for example, instead of this:
    
    >>> expFile = cmds.file( exportAll=1, preserveReferences=1 )
    
you can do this:

    >>> expFile = exportAll( preserveReferences=1)
    
some of the new commands were changed slightly from their flag name to avoid name clashes and to add to readability:

    >>> importFile( expFile )
    >>> createReference( expFile )

also note that the 'type' flag is set automatically for you when your path includes a '.mb' or '.ma' extension.
"""

try:
    import maya.cmds as cmds
except ImportError: pass

import path, sys
import core, util

def _getTypeFromExtension( path ):
    return {
        '.ma' : 'mayaAscii',
        '.mb' :    'mayaBinary'
    }[core.Path(path).ext]


       

def listNamespaces(root=None, recursive=False, internal=False):
    """Returns a list of the namespaces in the scene"""
    
    if root:
        curNS = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=root)
        namespaces = listNamespaces(internal=internal, recursive=recursive)
        cmds.namespace(set=":"+curNS)
        return namespaces
    
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    if not namespaces:
        return []
    
    if not internal:
        namespaces = sorted(set(namespaces) - set(["UI","shared"]))
        
    if recursive:
        childNamespaces = []
        for ns in namespaces:
            try:
                childNamespaces.extend(listNamespaces(recursive=True, root=ns))
            except: pass
        namespaces.extend(childNamespaces)
    
    return namespaces




def listReferences(type='list'):
    """file -q -reference
    By default returns a list of reference files as FileReference classes. The optional type argument can be passed a 'dict'
    (or dict object) to return the references as a dictionary with namespaces as keys and References as values.
    
    Untested: multiple references with no namespace...
    """
    
    # dict
    if type in ['dict', dict]:
        return getReferencesDict()
    
    # list
    return core._getAllFileReferences()

<<<<<<< .mine
def getReferencesDict():
    return dict((fr.fullNamespace, fr) for fr in core._getAllFileReferences())    

=======
def getReferences(reference=None, recursive=False):
    res = {}    
    if reference is None:
        for x in cmds.file( q=1, reference=1):
            try:
                ref = core.FileReference(x)
                res[ref.namespace] = ref
                if recursive:
                    res.update( ref.subReferences() )
            except: pass
    else:
        for x in cmds.file( self, q=1, reference=1):
            try:
                res[cmds.file( x, q=1, namespace=1)] = core.FileReference(x)
            except: pass
    return res    
>>>>>>> .r730
    
def createReference( *args, **kwargs ):
    """file -reference"""
    kwargs['reference'] = True
    try:
        return core.FileReference(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def loadReference( file, refNode, **kwargs ):
    """file -loadReference"""
    kwargs['loadReference'] = refNode
    try:
        return core.FileReference(cmds.file(file, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def unloadReference( file, refNode, **kwargs ):
    """file -unloadReference"""
    kwargs['unloadReference'] = refNode
    try:
        return core.FileReference(cmds.file(file, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg        
        
def exportAll( *args, **kwargs ):
    """file -exportAll"""
    kwargs['exportAll'] = True
    try:
        kwargs['type'] = _getTypeFromExtension(args[0])
    except KeyError: pass
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def exportAnim( *args, **kwargs ):
    """file -exportAnim"""
    kwargs['exportAnim'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def exportAnimFromReference( *args, **kwargs ):
    """file -exportAnimFromReference"""
    kwargs['exportAnimFromReference'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def exportAsReference( *args, **kwargs ):
    """file -exportAsReference"""
    kwargs['exportAsReference'] = True
    try:
        kwargs['type'] = _getTypeFromExtension(args[0])
    except KeyError: pass
    try:
        return core.FileReference(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg
    
def exportSelected( *args, **kwargs ):
    """file -exportSelected"""
    kwargs['exportSelected'] = True
    try:
        kwargs['type'] = _getTypeFromExtension(args[0])
    except KeyError: pass
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg
    
def exportSelectedAnim( *args, **kwargs ):
    """file -exportSelectedAnim"""
    kwargs['exportSelectedAnim'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg
    
def exportSelectedAnimFromReference( *args, **kwargs ):
    """file -exportSelectedAnimFromReference"""
    kwargs['exportSelectedAnimFromReference'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def importFile( *args, **kwargs ):
    """file -import"""
    kwargs['import'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def newFile( *args, **kwargs ):
    """file -newFile"""
    kwargs['newFile'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg

def openFile( *args, **kwargs ):
    """file -open"""
    kwargs['open'] = True
    try:
        return core.Path(cmds.file(*args, **kwargs))
    except RuntimeError, msg:
        raise IOError, msg    

def renameFile( *args, **kwargs ):
    """file -rename"""
    kwargs['rename'] = args[0]
    try:
        return core.Path(cmds.file(**kwargs))
    except RuntimeError, msg:
        raise IOError, msg
    
def saveAs(filepath, **kwargs):
    cmds.file( rename=filepath )
    kwargs['save']=True
    try:
        kwargs['type'] = _getTypeFromExtension(filepath)
    except KeyError: pass
    try:
        return core.Path(cmds.file(**kwargs))
    except RuntimeError, msg:
        raise IOError, msg