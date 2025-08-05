// Auto-generated test case: TC_006
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_006()
        {
          var paxList = new PaxList();
          var response = SubmitToNdcApi(paxList);
          Assert.IsTrue(response.Contains("at least one adult required"));
        }
    }
}
