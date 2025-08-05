// Auto-generated test case: TC_003
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_003()
        {
          var paxList = new PaxList
          {
            PassengerCodes = new List<string> { "ADT", "CHD", "GBE", "INF" }
          };
          var response = NdcApi.SubmitPaxList(paxList);
          Assert.IsTrue(response.IsSuccess);
        }
    }
}
