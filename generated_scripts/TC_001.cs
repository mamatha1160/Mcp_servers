// Auto-generated test case: TC_001
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_001()
        {
          var paxList = new PaxList();
          paxList.AddPassenger(PassengerType.ADT);
          paxList.AddPassenger(PassengerType.CHD);
          paxList.AddPassenger(PassengerType.GBE);
          paxList.AddPassenger(PassengerType.INF);
        
          var apiResponse = SubmitPaxListToNdcApi(paxList);
        
          Assert.IsTrue(apiResponse.IsSuccess);
        }
    }
}
