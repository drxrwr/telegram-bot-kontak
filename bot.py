import io
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

# Token dari BotFather
TOKEN = '7690676397:AAE3lCGg3S1Qt9hACCzYussdt3yDILFXHgg'

# Fungsi untuk memulai bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Kirimkan file TXT dan saya akan mengonversinya ke VCF.')

# Fungsi untuk menangani file yang dikirim oleh pengguna
def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    txt_content = file.download_as_bytearray().decode('utf-8')

    # Konversi TXT ke VCF
    vcf_content = convert_txt_to_vcf(txt_content)
    
    # Kirim file VCF ke pengguna
    bio = io.BytesIO()
    bio.write(vcf_content.encode('utf-8'))
    bio.seek(0)
    
    update.message.reply_document(document=InputFile(bio, filename="kontak.vcf"))

# Fungsi konversi TXT ke VCF
def convert_txt_to_vcf(txt_content, admin_name='Admin', navy_name='Navy', anggota_name='Anggota', numbering_enabled=True):
    lines = txt_content.split('\n')
    vcf_content = ""
    contact_index = 1
    for line in lines:
        line = line.strip()
        if line.isdigit():
            contact_name = f"Kontak-{contact_index}" if numbering_enabled else "Kontak"
            vcf_content += f"BEGIN:VCARD\nVERSION:3.0\nFN:{contact_name}\nTEL:+{line}\nEND:VCARD\n\n"
            contact_index += 1
    return vcf_content

def main():
    # Mengatur bot dengan token dari BotFather
    updater = Updater(TOKEN)
    
    # Daftar handler untuk menangani perintah /start dan file
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_file))

    # Memulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
