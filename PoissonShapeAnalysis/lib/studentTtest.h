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

#include <cmath>
#include <vector>

namespace ShapeAnalysis
{
  namespace detail
  {
    // Continued fraction used to evaluate the regularized incomplete beta
    // function (modified Lentz's method). See Numerical Recipes, 3rd ed.
    inline double incompleteBetaContinuedFraction(double a, double b, double x)
    {
      const int maxIterations = 200;
      const double epsilon = 3.0e-12;
      const double minimum = 1.0e-300;

      const double qab = a + b;
      const double qap = a + 1.0;
      const double qam = a - 1.0;

      double c = 1.0;
      double d = 1.0 - qab * x / qap;
      if (std::fabs(d) < minimum)
        {
        d = minimum;
        }
      d = 1.0 / d;
      double h = d;

      for (int m = 1; m <= maxIterations; ++m)
        {
        const int m2 = 2 * m;

        double aa = m * (b - m) * x / ((qam + m2) * (a + m2));
        d = 1.0 + aa * d;
        if (std::fabs(d) < minimum)
          {
          d = minimum;
          }
        c = 1.0 + aa / c;
        if (std::fabs(c) < minimum)
          {
          c = minimum;
          }
        d = 1.0 / d;
        h *= d * c;

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
        d = 1.0 + aa * d;
        if (std::fabs(d) < minimum)
          {
          d = minimum;
          }
        c = 1.0 + aa / c;
        if (std::fabs(c) < minimum)
          {
          c = minimum;
          }
        d = 1.0 / d;
        const double del = d * c;
        h *= del;

        if (std::fabs(del - 1.0) < epsilon)
          {
          break;
          }
        }

      return h;
    }

    // Regularized incomplete beta function I_x(a, b).
    inline double incompleteBetaRegularized(double a, double b, double x)
    {
      if (x <= 0.0)
        {
        return 0.0;
        }
      if (x >= 1.0)
        {
        return 1.0;
        }

      const double bt = std::exp(std::lgamma(a + b) - std::lgamma(a) - std::lgamma(b)
                                 + a * std::log(x) + b * std::log(1.0 - x));

      if (x < (a + 1.0) / (a + b + 2.0))
        {
        return bt * incompleteBetaContinuedFraction(a, b, x) / a;
        }
      return 1.0 - bt * incompleteBetaContinuedFraction(b, a, 1.0 - x) / b;
    }
  }// detail

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

    // Two-sided p-value of Student's t distribution:
    //   P(|T| > |t|) = I_{v / (v + t^2)}(v / 2, 1 / 2)
    double pValue = detail::incompleteBetaRegularized(0.5 * v, 0.5, v / (v + t_stat * t_stat));

    return pValue;
  };

}// ShapeAnalysis


#endif
