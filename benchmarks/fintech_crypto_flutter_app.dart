// ============================================================================
// Fintech & Crypto Mobile Application for Flutter (Dart 3.x)
// Demonstrating Clean Architecture, BLoC, Riverpod, Isolates, GoF, and Security
// ============================================================================

import 'dart:async';
import 'dart:isolate';
import 'package:flutter/material.dart';

// 1. Dart 3.x Sealed Class & ADT State Machine
sealed class WalletState {
  const WalletState();
}

class WalletInitial extends WalletState {
  const WalletInitial();
}

class WalletLoading extends WalletState {
  const WalletLoading();
}

class WalletSuccess extends WalletState {
  final String walletAddress;
  final double balanceBtc;
  const WalletSuccess({required this.walletAddress, required this.balanceBtc});

  WalletSuccess copyWith({String? walletAddress, double? balanceBtc}) {
    return WalletSuccess(
      walletAddress: walletAddress ?? this.walletAddress,
      balanceBtc: balanceBtc ?? this.balanceBtc,
    );
  }

  Map<String, dynamic> toJson() => {'address': walletAddress, 'balance': balanceBtc};
  factory WalletSuccess.fromJson(Map<String, dynamic> json) =>
      WalletSuccess(walletAddress: json['address'], balanceBtc: json['balance']);
}

class WalletFailure extends WalletState {
  final String error;
  const WalletFailure(this.error);
}

// 2. Command Intent Action Hierarchy
abstract class WalletEvent {}
class LoadWalletEvent extends WalletEvent {}
class TransferBtcEvent extends WalletEvent {
  final String toAddress;
  final double amount;
  TransferBtcEvent(this.toAddress, this.amount);
}

// 3. Modern Dart 3.x Records & Pattern Matching & Extension Types
extension type CryptoId(String id) {}

(double, double) calculateCryptoTax(double gross, double rate) {
  return (gross * rate, gross * (1.0 - rate));
}

String describeWalletState(WalletState state) {
  return switch (state) {
    WalletInitial() => 'Wallet Initialized',
    WalletLoading() => 'Loading blockchain records...',
    WalletSuccess(:final balanceBtc) when balanceBtc > 10.0 => 'Whale account loaded',
    WalletSuccess(:final balanceBtc) => 'Balance: $balanceBtc BTC',
    WalletFailure(:final error) => 'Error: $error',
  };
}

// 4. Enhanced Enums with Members & Methods
enum BlockchainNetwork {
  bitcoin('BTC', 1),
  ethereum('ETH', 2),
  solana('SOL', 3);

  final String ticker;
  final int chainId;
  const BlockchainNetwork(this.ticker, this.chainId);

  bool get isEvm => chainId == 2;
}

// 5. Mixin Horizontal Composition
mixin DiagnosticLogger on Object {
  void logTrace(String tag, String message) {
    debugPrint('[$tag] $message');
  }
}

// 6. Extension Method API Sugar
extension StringCryptoFormatting on String {
  String toMaskedAddress() {
    if (length < 10) return this;
    return '${substring(0, 6)}...${substring(length - 4)}';
  }
}

// 7. Clean Architecture UseCase Interactor
abstract class TransferFundsUseCase {
  Future<bool> call(String recipient, double amount);
}

class TransferFundsUseCaseImpl implements TransferFundsUseCase {
  final CryptoRepository repository;
  TransferFundsUseCaseImpl(this.repository);

  @override
  Future<bool> call(String recipient, double amount) async {
    return await repository.sendTransaction(recipient, amount);
  }
}

// 8. Structural Facade & Proxy Cached Repository
abstract class CryptoRepository {
  Future<bool> sendTransaction(String recipient, double amount);
  Future<WalletSuccess> fetchWallet();
}

class CryptoRepositoryProxy implements CryptoRepository {
  final CryptoRepository remoteSource;
  final Map<String, dynamic> localCache = {};

  CryptoRepositoryProxy(this.remoteSource);

  @override
  Future<bool> sendTransaction(String recipient, double amount) => remoteSource.sendTransaction(recipient, amount);

  @override
  Future<WalletSuccess> fetchWallet() async {
    if (localCache.containsKey('wallet')) {
      return localCache['wallet'] as WalletSuccess;
    }
    final fresh = await remoteSource.fetchWallet();
    localCache['wallet'] = fresh;
    return fresh;
  }
}

// 9. Concurrency: Isolate Heavy Cryptographic Verification
class CryptoHashWorker {
  static Future<String> computeSha256Parallel(String payload) async {
    return await compute(_hashPayloadInIsolate, payload);
  }

  static String _hashPayloadInIsolate(String input) {
    return '0000000000000000000' + input.hashCode.toRadixString(16);
  }

  Stream<int> streamBlockConfirmations() async* {
    for (int i = 1; i <= 6; i++) {
      await Future.delayed(const Duration(milliseconds: 100));
      yield i;
    }
  }

  Iterable<int> generateNonceSequence() sync* {
    int nonce = 0;
    while (nonce < 1000) {
      yield nonce++;
    }
  }
}

// 10. Creational: Singleton & Service Locator
class SystemEnvironmentConfig {
  static final SystemEnvironmentConfig instance = SystemEnvironmentConfig._internal();
  SystemEnvironmentConfig._internal();

  factory SystemEnvironmentConfig.fromMap(Map<String, dynamic> map) => instance;
}

// 11. Flutter UI Widget with Decorator, Composite, and Builder Pattern
class CryptoWalletCardWidget extends StatelessWidget {
  final Widget child;
  const CryptoWalletCardWidget({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: Colors.black87,
          borderRadius: BorderRadius.circular(16.0),
        ),
        child: ListView.builder(
          itemCount: 5,
          itemBuilder: (BuildContext ctx, int index) {
            return ListTile(title: Text('Tx #$index'));
          },
        ),
      ),
    );
  }
}

// 12. Security Hazard Detections: Async Gap Context & Hardcoded Secret
class DangerousWalletScreen extends StatefulWidget {
  const DangerousWalletScreen({super.key});

  @override
  State<DangerousWalletScreen> createState() => _DangerousWalletScreenState();
}

class _DangerousWalletScreenState extends State<DangerousWalletScreen> {
  final StreamController<double> _livePriceController = StreamController<double>();
  late String uninitializedWalletKey;

  Future<void> submitTransferDangerous(BuildContext context) async {
    await Future.delayed(const Duration(seconds: 2));
    // Hazard: using BuildContext across async gap without checking context.mounted
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

// Hardcoded private secret token hazard
const privateApiKey = "dpx_mock_secret_token_1234567890abcdef";
