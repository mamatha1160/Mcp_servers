// Auto-generated test case: TC_004
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_004()
        {
          var paxList = new PaxList { PtcCodes = new List<string> { "XYZ" } };
          var response = NdcApi.SubmitPaxList(paxList);
          Assert.IsTrue(response.IsSuccessStatusCode);
          Assert.AreEqual("invalid PTC code", response.ErrorMessage);
        }
    }
}
