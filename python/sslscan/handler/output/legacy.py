from sslscan import output
from sslscan.handler import Output

class Legacy(Output):
    short_description = "Legacy output (sslscan < 1.11)"
    description = """
    Support legacy output format
    """

    def __init__(self, foo=""):
        print(foo)

    def run(self, client, host_results):
        print("  Supported Client Cipher(s):")
        for cipher in client.get("ciphers", []):
            print("    %s" % cipher.get("name", ""))
        print("")

        for host in host_results:
            print("  Supported Server Cipher(s):")
            for cipher in host.get("ciphers", []):
                print(
                    "    %-9s %-6s %-9s %s" % (
                        cipher.get("status", "").capitalize(),
                        cipher.get("method.name", ""),
                        "%d bits" % cipher.get("bits", 0),
                        cipher.get("name", "")
                    )
                )
            print("")

            # renegotiation
            if host.get("renegotiation.supported", None) is not None:
                print("  TLS renegotiation:")
            if host.get("renegotiation.secure", None):
                print("    Secure session renegotiation supported")
            elif host.get("renegotiation.supported", None):
                print("    Insecure session renegotiation supported")
            elif host.get("renegotiation.supported", None) is not None:
                print("    Session renegotiation not supported\n\n");
            print("")

            print("  Preferred Server Cipher(s):")
            for cipher in host.get("ciphers.default", {}).values():
                if cipher is None:
                    continue
                print(
                    "    %-6s %-9s %s" % (
                        cipher.get("method.name", ""),
                        "%d bits" % cipher.get("bits", 0),
                        cipher.get("name", "")
                    )
                )
            x509 = host.get("certificate.x509", 0)
            print("")
            print("  SSL Certificate:")
            print("    Certificate blob:")
            print(x509.get_certificate_blob())
            print("    Version: %lu" % x509.get_version())
            tmp = x509.get_serial_number()
            print("    Serial Number: %lu (0x%lx)" % (tmp, tmp))
            print("    Signature Algorithm: %s" % x509.get_signature_algorithm())
            print("    Issuer: %s" % x509.get_issuer())
            print("    Not valid before: %s" % x509.get_not_before(3))
            print("    Not valid after: %s" % x509.get_not_before(3))
            print("    Subject: %s" % x509.get_subject())
            pk = x509.get_public_key()
            if pk:
                print("    Public Key Algorithm: %s" % pk.get_algorithm())
                tmp_name = pk.get_type_name()
                if tmp_name:
                    tmp_bits = pk.get_bits()
                    if tmp_bits:
                        print("    %s Public Key: (%d bit)" % (tmp_name, tmp_bits))
                    else:
                        print("    %s Public Key:" % tmp_name)
                    print(pk.get_key_print(6))
                else:
                    print("    Public Key: Unknown")
            else:
                print("   Public Key: Could not load")

            print("  Verify Certificate:")
            verfy_status = host.get("certificate.verify.status", None)
            if verfy_status:
                print("    Certificate passed verification")
            else:
                print("    %s" % host.get("certificate.verify.error_message", ""))


output.register("legacy", Legacy)
