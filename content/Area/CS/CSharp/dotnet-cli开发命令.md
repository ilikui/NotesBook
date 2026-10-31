# .NET CLI 开发命令

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MTkxMjMyNTU3

- C# 开发 <https://dotnet.microsoft.com/en-us/download>


- .NET CLI 是一个命令行界面，提供了一系列用于开发、构建、测试和发布.NET 应用程序的命令。这些命令统称为 dotnet 命令。它们允许开发者在各种操作系统上进行.NET 开发，而无需依赖于Visual Studio 等集成开发环境.﻿

- 下面是一些常用的 dotnet 命令：

- **项目和解决方案管理:**

  - dotnet new: 创建新的.NET项目或文件，例如控制台应用程序、类库等。

  - dotnet build: 编译.NET项目及其依赖项。

  - dotnet run: 运行.NET应用程序。

  - dotnet clean: 清理.NET项目的构建输出。

  - dotnet restore: 还原.NET项目所需的依赖项。

  - dotnet pack: 创建NuGet包。

  - dotnet publish: 发布.NET应用程序，生成可部署的文件。

  - dotnet test: 运行.NET项目的单元测试。

  - dotnet sln: 修改Visual Studio解决方案文件。﻿
- **NuGet 包管理:**

  - dotnet add package: 添加NuGet包引用到项目。

  - dotnet remove package: 从项目中删除NuGet包引用。

  - dotnet nuget add source: 添加NuGet源。

  - dotnet nuget list source: 列出所有配置的NuGet源。﻿
- **工具管理:**

  - dotnet tool install: 安装全局或本地的.NET工具。﻿

  - dotnet tool uninstall: 卸载全局或本地的.NET工具。﻿

  - dotnet tool list: 列出已安装的.NET工具。﻿
- **其他命令:**

  - dotnet help: 显示命令行帮助。

  - dotnet msbuild: 提供了对MSBuild命令行的访问。

  - dotnet format: 格式化代码。﻿
- **使用示例:**

  - 要创建一个新的控制台应用程序，可以运行 dotnet new console。

  - 要编译项目，可以运行 dotnet build。

  - 要运行应用程序，可以运行 dotnet run。

  - 要添加一个名为Newtonsoft.Json 的NuGet包，可以运行 dotnet add package Newtonsoft.Json。

  - 要安装一个名为dotnet-ef 的全局工具，可以运行 dotnet tool install --global dotnet-ef。﻿
- 通过使用 .NET CLI，开发者可以有效地管理.NET项目、构建、测试和部署应用程序，而无需依赖于特定的IDE。﻿


#Area/技术/CSharp