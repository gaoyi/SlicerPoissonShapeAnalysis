#include "lib/utilitiesIO.h"
#include "lib/SumOfTwoPoissonShapeAnalysis.h"

#include "itkPluginUtilities.h"

#include "PoissonShapeAnalysisCLP.h"

int main( int argc, char * argv[] )
{
  PARSE_ARGS;

  const unsigned int ImageDim = 3;
  typedef short pixel_t;
  typedef itk::Image<pixel_t, ImageDim> image_t;

  // Read in two groups of images
  std::vector< image_t::Pointer > shapeList1 = ShapeAnalysis::readImageSeries<image_t>(shapeNameList1);
  std::vector< image_t::Pointer > shapeList2 = ShapeAnalysis::readImageSeries<image_t>(shapeNameList2);

  typedef ShapeAnalysis::SumOfTwoPoissonShapeAnalysis<image_t> SumOfTwoPoissonShapeAnalysisType;
  SumOfTwoPoissonShapeAnalysisType poissonShapeAnalysis;

  poissonShapeAnalysis.SetShapeGroup1(shapeList1);
  poissonShapeAnalysis.SetShapeGroup2(shapeList2);
  poissonShapeAnalysis.setPerformRegistration(doRegistration);

  poissonShapeAnalysis.update();

  ShapeAnalysis::writeImage<SumOfTwoPoissonShapeAnalysisType::FloatImageType>(poissonShapeAnalysis.getMeanShapeImage(), meanImageName.c_str());
  ShapeAnalysis::writePolydataToXMLFile<char>(meanVTKName.c_str(), poissonShapeAnalysis.getMeanShapeSurface());

  return EXIT_SUCCESS;
}

