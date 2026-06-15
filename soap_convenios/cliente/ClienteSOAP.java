import java.net.URL;
import java.io.OutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.util.Scanner;

public class ClienteSOAP {

    static String chamarSOAP(String xml) throws Exception {
        URL url = new URL("http://localhost:8003/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "text/xml; charset=utf-8");
        conn.setDoOutput(true);

        OutputStream os = conn.getOutputStream();
        os.write(xml.getBytes("UTF-8"));
        os.flush();

        InputStream is;
        try {
            is = conn.getInputStream();
        } catch (Exception e) {
            is = conn.getErrorStream();
        }

        Scanner scanner = new Scanner(is, "UTF-8");
        String resposta = scanner.useDelimiter("\\A").next();
        scanner.close();
        return resposta;
    }

    public static void main(String[] args) throws Exception {

        System.out.println("=== Listando planos aceitos ===");
        String xmlListar = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tns=\"clinica.convenio\"><soapenv:Body><tns:listar_planos_aceitos/></soapenv:Body></soapenv:Envelope>";
        System.out.println(chamarSOAP(xmlListar));

        System.out.println("\n=== Cadastrando convênio ===");
        String xmlCadastrar = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tns=\"clinica.convenio\"><soapenv:Body><tns:cadastrar_convenio><tns:cpf>999.888.777-66</tns:cpf><tns:plano>Amil</tns:plano></tns:cadastrar_convenio></soapenv:Body></soapenv:Envelope>";
        System.out.println(chamarSOAP(xmlCadastrar));

        System.out.println("\n=== Verificando convênio válido ===");
        String xmlVerificar = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tns=\"clinica.convenio\"><soapenv:Body><tns:verificar_convenio><tns:cpf>999.888.777-66</tns:cpf><tns:plano>Amil</tns:plano></tns:verificar_convenio></soapenv:Body></soapenv:Envelope>";
        System.out.println(chamarSOAP(xmlVerificar));
    }
}