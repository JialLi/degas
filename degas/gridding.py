import gbtpipe
import glob
import os
import pkg_resources
from . import catalogs
from . import postprocess


def gridBlocks(release='QA0', edgetrim = 100,
               basebuff = 64,
               datadir='/lustre/pipeline/scratch/DEGAS/',
               setup='13CO_C18O'):

    """
    This builds tiny maps suitable for QA1 of blocks
    """

    pipeversion = pkg_resources.get_distribution("degas").version
    filelist = glob.glob(datadir + galaxy + '/' +
                         setup + '/*fits')

def gridGalaxy(galaxy='IC0342', setup='13CO_C18O',
               datadir='/lustre/pipeline/scratch/DEGAS/',
               overwrite=True, release='QA1', edgetrim = 100,
               basebuff = 64, plotTimeSeries=True, PostprocOnly=False,
               **kwargs):

    pipeversion = pkg_resources.get_distribution("degas").version


    # Note that we also use a few channels in the middle.

    filelist = glob.glob(datadir + galaxy + '/' +
                         setup + '/*fits')
    OutputDirectory = datadir + galaxy + '/images/'

    if not os.access(OutputDirectory, os.W_OK):
        try:
            os.mkdir(OutputDirectory)
            os.chdir(OutputDirectory)
        except OSError:
            raise
    if '12CO' in setup:
        filename = galaxy + '_' + setup + '_v{0}'.format(pipeversion)
        if not PostprocOnly:
            gbtpipe.griddata(filelist,
                             startChannel=edgetrim,
                             endChannel=1024-edgetrim,
                             baselineRegion = [slice(edgetrim,
                                                     edgetrim+basebuff,1),
                                               slice(1024-edgetrim-basebuff,
                                                     1024-basebuff,1)],
                             outdir=OutputDirectory,
                             flagRMS=True, plotTimeSeries=plotTimeSeries,
                             flagRipple=True, pixPerBeam=4.0,
                             plotsubdir='timeseries',
                             outname=filename, **kwargs)
        postprocess.cleansplit(OutputDirectory
                               + filename + '.fits',
                               spectralSetup=setup,
                               HanningLoops=1,
                               spatialSmooth=1.3, **kwargs)
    else:
        filename = galaxy + '_' + setup + '_v{0}'.format(pipeversion)
        if not PostprocOnly:
            gbtpipe.griddata(filelist,
                             startChannel=edgetrim,
                             endChannel=1024-edgetrim,
                             baselineRegion = [slice(edgetrim,
                                                     edgetrim+basebuff,1),
                                               slice(448,576,1),
                                               slice(1024-edgetrim-basebuff,
                                                     1024-basebuff,1)],
                             outdir=OutputDirectory,
                             blorder=5,
                             flagRMS=True,  plotTimeSeries=plotTimeSeries,
                             flagRipple=True, pixPerBeam=4.0,
                             plotsubdir='timeseries',
                             outname=filename, **kwargs)

        postprocess.cleansplit(OutputDirectory
                               + filename + '.fits',
                               spectralSetup=setup,
                               HanningLoops=1,
                               spatialSmooth=1.3, **kwargs)
        

    
