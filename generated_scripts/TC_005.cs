// Auto-generated test case: TC_005
using NUnit.Framework;

namespace NdcTests
{
    [TestFixture]
    public class NdcTestCases
    {
        public void TC_005()
        {
          var paxList = new PaxList();
          paxList.Adults = new List<Adult> { new Adult() };
          paxList.Infants = new List<Infant> { new Infant(), new Infant() };
          var response = SubmitPaxListToNDCApi(paxList);
          Assert.IsTrue(response.IsSuccessStatusCode == false);
          Assert.AreEqual("maximum one infant per adult", response.ErrorMessage);
        }
    }
}
