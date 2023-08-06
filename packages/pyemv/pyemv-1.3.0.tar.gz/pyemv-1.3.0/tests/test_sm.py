import pytest

from pyemv import sm


def test_generate_command_mac_exception() -> None:
    # SK < 16 bytes
    with pytest.raises(
        ValueError,
        match="Session Key must be a double length DES key",
    ):
        sm.generate_command_mac(
            sk_smi=bytes.fromhex("AAAAAAAAAAAAAAAA"),
            command=bytes.fromhex("12345678901214"),
        )

    # SK > 16 bytes
    with pytest.raises(
        ValueError,
        match="Session Key must be a double length DES key",
    ):
        sm.generate_command_mac(
            sk_smi=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC"),
            command=bytes.fromhex("12345678901214"),
        )


def test_encrypt_command_data_mastercard_nonpadded() -> None:
    # If MasterCard data is not multiple of 8 bytes
    # then it has to be padded with 0x80 and 0x00 until
    # it is multiple of 8 bytes.
    # if the data is multiple of 8 bytes then no padding
    # is required.

    no_padding_required = sm.encrypt_command_data(
        sk_smc=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
        command_data=bytes.fromhex("1234800000000000"),
        encryption_type=sm.EncryptionType.MASTERCARD,
    )

    padding_required = sm.encrypt_command_data(
        sk_smc=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
        command_data=bytes.fromhex("1234"),
        encryption_type=sm.EncryptionType.MASTERCARD,
    )

    assert no_padding_required == padding_required


def test_encrypt_command_data_exception() -> None:
    # SK < 16 bytes
    with pytest.raises(
        ValueError,
        match="Session Key must be a double length DES key",
    ):
        sm.encrypt_command_data(
            sk_smc=bytes.fromhex("AAAAAAAAAAAAAAAA"),
            command_data=bytes.fromhex("12345678901214"),
            encryption_type=sm.EncryptionType.VISA,
        )

    # SK > 16 bytes
    with pytest.raises(
        ValueError,
        match="Session Key must be a double length DES key",
    ):
        sm.encrypt_command_data(
            sk_smc=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC"),
            command_data=bytes.fromhex("12345678901214"),
            encryption_type=sm.EncryptionType.VISA,
        )

    # Invalid encryption type
    with pytest.raises(
        TypeError,
        match="Encryption type must be EncryptionType Enum, not dict",
    ):
        sm.encrypt_command_data(
            sk_smc=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
            command_data=bytes.fromhex("12345678901214"),
            encryption_type={},  # type: ignore
        )


def test_format_vis_pin_block_exception() -> None:
    # PIN < 4 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
            pin=b"123",
        )

    # PIN > 12 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
            pin=b"1234567890123",
        )

    # ICC MK AC < 16 bytes
    with pytest.raises(
        ValueError,
        match="ICC Master Key for AC must be a double length DES key",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAA"),
            pin=b"123456789012",
        )

    # ICC MK AC > 16 bytes
    with pytest.raises(
        ValueError,
        match="ICC Master Key for AC must be a double length DES key",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC"),
            pin=b"123456789012",
        )

    # Current PIN < 4 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
            pin=b"1234",
            current_pin=b"123",
        )

    # Current PIN > 12 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_vis_pin_block(
            icc_mk_ac=bytes.fromhex("AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB"),
            pin=b"1234",
            current_pin=b"1234567890123",
        )


def test_format_iso9564_2_pin_block_exception() -> None:
    # PIN < 4 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_iso9564_2_pin_block(pin=b"123")

    # PIN > 12 bytes
    with pytest.raises(
        ValueError,
        match="PIN must be between 4 and 12 digits long",
    ):
        sm.format_iso9564_2_pin_block(pin=b"1234567890123")
