// Auto-generated test case: TC_002
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_002()
        {
          var paxList = new PaxList();
          paxList.AddPassenger(new Passenger { PaxID = "123" });
          paxList.AddPassenger(new Passenger { PaxID = "123" });
          var apiResponse = SubmitToNdcApi(paxList);
          Assert.IsTrue(apiResponse.IsSuccessStatusCode);
          Assert.AreEqual("duplicate PaxID", apiResponse.ErrorMessage);
        }
    }
}
