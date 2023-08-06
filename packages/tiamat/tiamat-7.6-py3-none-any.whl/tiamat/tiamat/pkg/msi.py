import os
import shutil


class MSIError(Exception):
    pass


class WIXError(MSIError):
    pass


RAW_WXS_ZML = """<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
<Product Id="*" UpgradeCode="{}"
Name="{}" Version="{}" Manufacturer="{}" Language="{}">
<Package InstallerVersion="{}" Compressed="{}" Comments="{}"/>
<Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
<Directory Id="TARGETDIR" Name="SourceDir">
<Directory Id="ProgramFilesFolder">
<Directory Id="INSTALLDIR" Name="{}">
<Component Id="ApplicationFiles" Guid="{}">
<File Id="ApplicationFile1" Source="dist\\{}.exe"/>
</Component>
</Directory>
</Directory>
</Directory>
<Feature Id="DefaultFeature" Level="1">
<ComponentRef Id="ApplicationFiles"/>
</Feature>
</Product>
</Wix>"""


def build(hub, bname: str):
    """
    Build a new package using msi.

    :param bname: The name of the build configuration to use from the build.conf file.
    """

    opts = hub.tiamat.BUILDS[bname]
    pkg = dict(opts.pkg)

    # get candle or light path
    if pkg.get("candle_path") is None:
        pkg["candle_path"] = pkg.get("light_path")
    elif pkg.get("light_path") is None:
        pkg["light_path"] = pkg.get("candle_path")

    # candle path can't be None
    if pkg.get("candle_path") is None:
        raise MSIError("'candle_path' and 'light_path' both can't be None!")

    # get file_name
    file_name = opts.name
    if pkg.get("wxs_override") is not None:
        file_name = pkg.get("wxs_override")
    elif pkg.get("wixobj_override") is not None:
        file_name = pkg.get("wixobj_override")

    # remove file extension
    if "." in file_name:
        file_name = ".".join(file_name.split(".")[:-1])

    if pkg.get("wxs_override") is not None:  # wxs override MSI build
        _gen_wixobj(hub, pkg["candle_path"], pkg["wxs_override"])

        _build_msi(hub, pkg["light_path"], file_name + ".wixobj")
        _clean_file(file_name + ".wixobj")
    elif pkg.get("wixobj_override") is not None:  # wixobj override MSI build
        _build_msi(hub, pkg["light_path"], pkg["wixobj_override"])
    else:  # Normal MSI build
        settings = {"name": file_name}
        for setting_name in (
            "upgrade_code",
            "version",
            "manufacturer",
            "language",
            "package_installer_version",
            "compressed",
            "comments",
            "guid",
        ):
            if setting_name in pkg:
                settings[setting_name] = pkg[setting_name]

        _gen_wxs_xml(**settings)
        _gen_wixobj(hub, pkg["candle_path"], file_name + ".wxs")
        _build_msi(hub, pkg["light_path"], file_name + ".wixobj")
        _clean_file(file_name + ".wxs")
        _clean_file(file_name + ".wixobj")

    _clean_file(file_name + ".wixpdb")

    # Make msi_build dir
    try:
        if not os.path.isdir("msi_build"):
            os.mkdir("msi_build")
    except OSError:
        raise MSIError("Can't make msi_build dir")

    # Move msi to msi_build dir
    for f in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), f)):
            if f.split(".")[-1] == "msi":
                try:
                    shutil.move(f, "msi_build")
                except shutil.Error:
                    try:
                        os.remove(os.path.join("msi_build", f))
                    except OSError:
                        raise MSIError("Can't move msi to msi_build dir")
                    shutil.move(f, "msi_build")


def _gen_wxs_xml(
    upgrade_code: str = "12345678-1234-1234-1234-111111111111",
    name: str = "",
    version: str = "0.0.1",
    manufacturer: str = "Company Name",
    language: str = "1033",
    package_installer_version: str = "200",
    compressed: str = "yes",
    comments: str = "SaltStack",
    guid: str = "12345678-1234-1234-1234-222222222222",
):
    """
    :param upgrade_code:
    :param name: The name of the project to build.
    :param version:
    :param manufacturer:
    :param language:
    :param package_installer_version:
    :param compressed:
    :param comments:
    :param guid:
    """
    raw_xml = RAW_WXS_ZML.format(
        upgrade_code,
        name,
        version,
        manufacturer,
        language,
        package_installer_version,
        compressed,
        comments,
        name,
        guid,
        name,
    )

    with open(f"{name}.wxs", "w") as file:
        file.write(raw_xml)


def _gen_wixobj(hub, candle_path: str, wxs_file: str):
    """
    :param candle_path:
    :param wxs_file:
    """
    hub.tiamat.cmd.run(
        [os.path.join(candle_path, "candle.exe"), wxs_file],
        fail_on_error=True,
    )


def _build_msi(hub, light_path: str, wixobj_file: str):
    hub.tiamat.cmd.run(
        [os.path.join(light_path, "light.exe"), wixobj_file],
        fail_on_error=True,
    )


def _clean_file(file: str):
    try:
        os.remove(file)
    except OSError:
        pass
