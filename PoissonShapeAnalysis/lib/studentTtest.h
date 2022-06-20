/*******************************************************************************/
/*                                                                             */
/*  Copyright (c) 2010, Yi Gao, Zhenkai Ou                                     */
/*  gaoyi@gatech.edu                                                           */
/*                                                                             */
/*                                                                             */
/*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR */
/*  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,   */
/*  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL    */
/*  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER */
/*  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING    */
/*  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER        */
/*  DEALINGS IN THE SOFTWARE.                                                  */
/*                                                                             */
/*  See the README.md and COPYING files for usage and copyright information.   */
/*                                                                             */
/*******************************************************************************/


#ifndef studentTtest_h_
#define studentTtest_h_

#include <vector>

#include <boost/math/distributions/students_t.hpp>

namespace ShapeAnalysis
{
  template< typename valueType >
  double studentTTest(const std::vector<valueType>& array1, const std::vector<valueType>& array2)
  {
    unsigned count1, count2;
    double sum1 = 0, sum2 = 0, Sm1, Sm2, Sd1, Sd2, tempsum1 = 0, tempsum2 = 0;
    unsigned Sn1, Sn2;
    // Sm1 = Sample 1 Mean.
    // Sd1 = Sample 1 Standard Deviation.
    // Sn1 = Sample 1 Size.
    // Sm2 = Sample 2 Mean.
    // Sd2 = Sample 2 Standard Deviation.
    // Sn2 = Sample 2 Size.

    for (count1 = 0; count1 < array1.size(); count1++)
      {
        sum1 = sum1 + array1[count1];
      }
    Sn1 = array1.size();
    Sm1 = sum1 / Sn1;

    for (count1 = 0; count1 < array1.size(); count1++)
      {
        tempsum1 = tempsum1 + (array1[count1] - Sm1) * (array1[count1] - Sm1);
      }
    Sd1 = sqrt(tempsum1 / (Sn1 - 1));

    for (count2 = 0; count2 < array2.size(); count2++)
      {
        sum2 = sum2 + array2[count2];
      }
    Sn2 = array2.size();
    Sm2 = sum2 / Sn2;

    for (count2 = 0; count2 < array2.size(); count2++)
      {
        tempsum2 = tempsum2 + (array2[count2] - Sm2) * (array2[count2] - Sm2);
      }
    Sd2 = sqrt(tempsum2 / (Sn2 - 1));

    double v = Sn1 + Sn2 - 2.0;
    double sp = sqrt(((Sn1 - 1) * Sd1 * Sd1 + (Sn2 - 1) * Sd2 * Sd2) / v);
    double t_stat = (Sm1 - Sm2) / (sp * sqrt(1.0 / Sn1 + 1.0 / Sn2));
    boost::math::students_t dist(v);
    double q = boost::math::cdf(boost::math::complement(dist, fabs(t_stat)));
    double pValue = 2.0 * q;

    return pValue;
  };

}// ShapeAnalysis


#endif
