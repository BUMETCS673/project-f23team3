/**
* JetBrains Space Automation
* This Kotlin script file lets you automate build activities
* For more info, see https://www.jetbrains.com/help/space/automation.html
*/

job("Qodana") {
   startOn {
      gitPush {
         branchFilter {
            +"refs/heads/Customer"
         }
      }
   }
   container("jetbrains/qodana-python:latest") {
       env["QODANA_TOKEN"] = Secrets("qodana-token")
       shellScript {
           content = """
               qodana
               """.trimIndent()
      }
   }
}
